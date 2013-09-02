from django.contrib import messages
from django.db import connections
from django.views.generic import View
from django.shortcuts import render
from sqlconsole.forms import SQLConsoleForm


class SQLConsoleView(View):
    form_class = SQLConsoleForm
    initial = {'key': 'value'}
    template_name = 'sqlconsole.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            connection = connections['postgres_gijs']
            cursor = connection.cursor()
            data = []
            description = []
            try:
                cursor.execute(form.data['query'])
                if cursor.rowcount > 1000:
                    messages.error(request, "too many rows (>1000), please LIMIT your query")
                else:
                    data = cursor.fetchall()
                    description = cursor.description
            except connection.connection.InternalError as e:
                messages.error(request, str(e))


            context = {
                'form': form,
                'data': data,
                'description': description,
            }
            return render(request, self.template_name, context)