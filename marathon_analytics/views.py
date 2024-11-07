from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Result
import plotly
import plotly.graph_objs as go
import math
# Create your views here.
class ResultsListView(ListView):
    '''View to display list of marathon results.'''

    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = "results"
    paginate_by = 50
    def get_queryset(self) -> QuerySet[any]:
        qs = super().get_queryset()
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if city: 
                qs = Result.objects.filter(city__icontains=city)
        return qs
    
class ResultDetailView(DetailView):
    '''View to show detail page for one result.'''
    template_name = 'marathon_analytics/result_detail.html'
    model = Result
    context_object_name = 'r'
    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''
        context = super().get_context_data(**kwargs)
        r = context['r']
        # start with superclass context
        x = [f'Runners Passed by {r.first_name}', f'Runners who passed {r.first_name}']
        y = [r.get_runners_passed(), r.get_runners_passed_by()]
        fig = go.Bar(x=x, y=y)
        # fig = go.Bar(x=x, y=y)
        # fig = go.Pie(labels=['a', 'b', 'c'], 
        #              values = [0.4, 0.2, 0.4])
        graph_div = plotly.offline.plot({"data": [fig]}, auto_open=False, output_type="div")
        # graph_div = plotly.offline.plot({"data": [fig],}, auto_open=False, output_type="div")
        context['graph_div'] = graph_div
        # create graph of first half/second half as pie chart:
        x = ['first half', 'second half']
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second
        y = [first_half_seconds , second_half_seconds]
        
        # generate the Pie chart
        fig = go.Pie(labels=x, values=y) 
        title_text = f"Half Marathon Splits"
        # obtain the graph as an HTML div"
        graph_div_splits = plotly.offline.plot({"data": [fig], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        # send div as template context variable
        context['graph_div_splits'] = graph_div_splits
        return context
