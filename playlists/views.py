from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Playlist, Artist, Album, Song,Genre
from .forms import NewPlaylist, AddSong
from comments.forms import NewComment

class PlaylistIndex(ListView):
    model = Playlist
    queryset = Playlist.objects.order_by('-date_created')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewPlaylist()
        context['genres'] = Genre.objects.all()
        return context

class PlaylistDetail(DetailView):
    model = Playlist
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = NewComment()
        context['song_form'] = AddSong()
        return context

class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['title','description']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlaylistUpdate(UpdateView):
    model = Playlist
    fields = ['title','songs','description']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlaylistDelete(DeleteView):
    model = Playlist
    success_url = '/'
    def test_func(self):
        pl = self.get_object()
        if pl.user == self.request.user:
            return True
        else:
            return False

class GenreList(ListView):
    model = Genre
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewPlaylist()
        context['genres'] = Genre.objects.all()
        return context
    def get_queryset(self):
        self.genre = get_object_or_404(Genre, name=self.kwargs['name'])
        return Genre.objects.get(name=self.genre).playlist_set.all()

# class UserList(ListView):
#     model = User
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = NewPlaylist()
#         context['genres'] = Genre.objects.all()
#         return context
#     def get_queryset(self):
#         self.user = get_object_or_404(User, name=self.kwargs['username'])
#         return Genre.objects.get(name=self.genre).playlist_set.all()

def add_song_to_pl(req,pk):
    pl = Playlist.objects.get(pk=pk)
    if req.method == "POST":
        f = AddSong(req.POST)
        if f.is_valid():
            if req.user == pl.user:
                (artist, album, title) = (f.cleaned_data['artist'], f.cleaned_data['album'],f.cleaned_data['title'])
                try:
                    ar = Artist.objects.get(name=artist)
                except:
                    ar = Artist(name=artist)
                    ar.save()
                try:
                    al = Album.objects.get(title=album)
                except:
                    al = Album(title=album,artist=ar)
                    al.save()
                try:
                    son = Song.Objects.get(title=title)
                except:
                    son = Song(title=title,artist=ar,album=al)
                    son.save()
                finally:
                    pl.songs.add(son)
                    pl.save()
            return redirect('playlists-detail', pk)
