from django.contrib import messages
from django.db import connections
from django.views.generic import View
from django.shortcuts import render
from sqlconsole.forms import SQLConsoleForm
from sqlconsole.db import check_database
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class SQLConsoleView(View):
    form_class = SQLConsoleForm
    initial = {'key': 'value'}
    template_name = 'sqlconsole.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SQLConsoleView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        db_name = self.kwargs.get('db', 'default')
        check_database(db_name)
        form = self.form_class(initial=self.initial)
        context = {
            'form': form,
            'db_name': db_name,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        db_name = self.kwargs.get('db', 'default')
        check_database(db_name)
        if form.is_valid():
            connection = connections[db_name]
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
                'db_name': db_name
            }
            return render(request, self.template_name, context)