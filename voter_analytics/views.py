from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Voter
import plotly
import plotly.graph_objs as go
import math
from django.db.models import Min, Max

# Create your views here.
class VotersListView(ListView):
    '''View to display list of voter results.'''

    template_name = 'voter_analytics/results.html'
    model = Voter
    context_object_name = "voters"
    paginate_by = 100
    
    def get_queryset(self) -> QuerySet[any]:
        qs = super().get_queryset()
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                qs = qs.filter(party_affiliation__icontains=party)
        
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                qs = qs.filter(dob__gte=min_dob)
        
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                qs = qs.filter(dob__lte=max_dob)
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                qs = qs.filter(voter_score=score)
        if 'v20state' in self.request.GET:
            v20 = self.request.GET['v20state']
            if v20:
                qs = qs.filter(v20state=v20)
        if 'v21town' in self.request.GET:
            v21T = self.request.GET['v21town']
            if v21T:
                qs = qs.filter(v21town=v21T)
        if 'v21primary' in self.request.GET:
            v21P = self.request.GET['v21primary']
            if v21P:
                qs = qs.filter(v21primary=v21P)
        if 'v22general' in self.request.GET:
            v22G = self.request.GET['v22general']
            if v22G:
                qs = qs.filter(v22general=v22G)
        if 'v23town' in self.request.GET:
            v23T = self.request.GET['v23town']
            if v23T:
                qs = qs.filter(v23town=v23T)
        return qs
    def get_years(self):
        years = []
        min_dob = Voter.objects.aggregate(Min('dob'))['dob__min']
        max_dob = Voter.objects.aggregate(Max('dob'))['dob__max']
        for i in range(min_dob.year, max_dob.year + 1):
            years.append(i)
        return years

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = self.get_years() 
        return context
class VoterDetailView(DetailView):
    '''View to show detail page for one result.'''
    template_name = 'voter_analytics/result_detail.html'
    model = Voter
    context_object_name = 'r'

class GraphsListView(ListView):
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'r'
    def get_queryset(self) -> QuerySet[any]:
        qs = super().get_queryset()
        if 'party_affiliation' in self.request.GET:
            party = self.request.GET['party_affiliation']
            if party:
                qs = qs.filter(party_affiliation=party)
        
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                qs = qs.filter(dob__gte=min_dob)
        
        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                qs = qs.filter(dob__lte=max_dob)
        if 'voter_score' in self.request.GET:
            score = self.request.GET['voter_score']
            if score:
                qs = qs.filter(voter_score=score)
        if 'v20state' in self.request.GET:
            v20 = self.request.GET['v20state']
            if v20:
                qs = qs.filter(v20state=v20)
        if 'v21town' in self.request.GET:
            v21T = self.request.GET['v21town']
            if v21T:
                qs = qs.filter(v21town=v21T)
        if 'v21primary' in self.request.GET:
            v21P = self.request.GET['v21primary']
            if v21P:
                qs = qs.filter(v21primary=v21P)
        if 'v22general' in self.request.GET:
            v22G = self.request.GET['v22general']
            if v22G:
                qs = qs.filter(v22general=v22G)
        if 'v23town' in self.request.GET:
            v23T = self.request.GET['v23town']
            if v23T:
                qs = qs.filter(v23town=v23T)
        return qs
    def get_years(self):
        years = []
        min_dob = Voter.objects.aggregate(Min('dob'))['dob__min']
        max_dob = Voter.objects.aggregate(Max('dob'))['dob__max']
        for i in range(min_dob.year, max_dob.year + 1):
            years.append(i)
        return years

    def get_context_data(self, **kwargs) :
        '''
        Provide context variables for use in template
        '''
        context = super().get_context_data(**kwargs)
        r = context['r']
        context['years'] = self.get_years() 
        voters_queryset = self.get_queryset()
        all_years = voters_queryset.all().values('dob')
        x = [dob['dob'].year for dob in all_years]
        fig = go.Histogram(
            x=x,
            nbinsx=200,
            marker=dict(color='blue')
        )
        title_text = f'Voter Distribution by Year of Birth (n={voters_queryset.count()})'
        
        graph_div = plotly.offline.plot({"data": [fig], "layout_title_text": title_text}, auto_open=False, output_type="div")
        # graph_div = plotly.offline.plot({"data": [fig],}, auto_open=False, output_type="div")
        context['graph_div'] = graph_div
        x = ['R', 'D', 'U', 'CC', 'L', 'T', 'O', 'G', 'J', 'Q', 'FF']
        d_voters = voters_queryset.filter(party_affiliation__icontains='D').count()
        r_voters = voters_queryset.filter(party_affiliation__icontains='R').count()
        u_voters = voters_queryset.filter(party_affiliation__icontains='U').count()
        cc_voters = voters_queryset.filter(party_affiliation__icontains='CC').count()
        l_voters = voters_queryset.filter(party_affiliation__icontains='L').count()
        t_voters = voters_queryset.filter(party_affiliation__icontains='T').count()
        o_voters = voters_queryset.filter(party_affiliation__icontains='O').count()
        g_voters = voters_queryset.filter(party_affiliation__icontains='G').count()
        j_voters = voters_queryset.filter(party_affiliation__icontains='J').count()
        q_voters = voters_queryset.filter(party_affiliation__icontains='Q').count()
        ff_voters = voters_queryset.filter(party_affiliation__icontains='FF').count()
        y = [r_voters, d_voters, u_voters, cc_voters, l_voters, t_voters, o_voters, g_voters, j_voters, q_voters, ff_voters]
        party_counts = [voters_queryset.filter(party_affiliation=party).count() for party in x]
        fig_2 = go.Pie(labels=x, values=y) 
        title_text = f"Voter Party Affiliation (n={voters_queryset.count()})"
        graph_div_splits = plotly.offline.plot({"data": [fig_2], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")
        context['graph_div_splits'] = graph_div_splits
        voters_20 = voters_queryset.filter(v20state=True).count()
        voters_21T = voters_queryset.filter(v21town=True).count()
        voters_21P = voters_queryset.filter(v21primary=True).count()
        voters_22 = voters_queryset.filter(v22general=True).count()
        voters_23 = voters_queryset.filter(v23town=True).count()
        x = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        y = [voters_20, voters_21T, voters_21P, voters_22, voters_23]
        fig_3 = go.Bar(
                x=x,
                y=y,
                marker=dict(color='blue')
            )
        title_text = f'Voter Count by Election (n={voters_queryset.count()})'

        graph_div_elect = plotly.offline.plot({"data": [fig_3],  "layout_title_text": title_text}, auto_open=False, output_type="div")
        context['graph_div_elect'] = graph_div_elect

        

        return context
    