from django.shortcuts import render
from django.views.generic import View, RedirectView
from .forms import SearchForm
from .api_interations import search_recipe, get_recipe
from .models import Recipe, Ingredient
# Create your views here.


class SearchRecipes(View):
    template_name = 'main/search.html'

    def get(self,request, *args, **kwargs): ## request.method==GET
        return render(request, self.template_name, {'form': SearchForm()})

    def post(self, request, *args, **kwargs): ## request.method==POST
        form = SearchForm(request.POST)
        if form.valid(self):
            data = search_recipe(form.cleaned_data['text'])
        else:
            data=None
        return render(request, self.template_name, {'form': form, 'recipe_list': data})

class FetchDataToDB(RedirectView):
    pattern_name = 'search'

    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs['id']
        data = get_recipe(id)
        print(data.keys)
        r = Recipe.objects.create(
            spoon_id=data['id'],
            ingredients=data['extendedIngredients'],
            title= data['title'],
            ready_minutes = data['readyInMinutes'],
            servings = data['servings'],
            image = data['image'],
            summary = data['summary'],
            instructions = data['instructions']
        )

        self.request.user.profile.common_recipes.add(r)  ## r.profile_set.add(self.request.user.profile)
        return super().get_redirect_url()
