from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Board, Document ,Subject
from .forms import NewDocumentForm,NewSubjectForm
from django.contrib.auth.decorators import login_required
from .decorators import student_required,moderator_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

def home(request):
	boards=Board.objects.all()
	return render(request,'home.html',{'boards':boards})

def board_documents(request, pk):
    board = get_object_or_404(Board, pk=pk)
    subjects= Subject.objects.all()
    check = []
    for subject in subjects:
        check.append(Document.objects.filter(is_reviewed="False",subject=subject))
    news=zip(subjects,check)
    return render(request,'subjects.html',{'board': board ,'subjects':news })

def subjects(request,pk1,pk2):
    board = get_object_or_404(Board, pk=pk1)
    subject=get_object_or_404(Subject, pk=pk2)
    queryset = subject.documents.order_by('-uploaded_at').annotate(replies=Count('document') - 1)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 12)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        documents = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        documents = paginator.page(paginator.num_pages)
    return render(request, 'documents.html', {'board': board ,'subject' : subject , 'documents' : documents})

@login_required
@moderator_required
def new_subject(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewSubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.board = board
            subject.created_by = request.user
            subject.save()
            return redirect('board_documents', pk=pk)  # TODO: redirect to the created topic page
    else:
        form = NewSubjectForm()
    return render(request, 'new_subject.html', {'board': board, 'form': form})



@login_required
@student_required
def new_document(request, pk1, pk2):
    board = get_object_or_404(Board, pk=pk1)
    subject = get_object_or_404(Subject, pk=pk2)
    if request.method == 'POST':
        form = NewDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document=form.save(commit=False)
            document.subject=subject
            document.subject.board=board
            document.uploaded_by=request.user.student
            document.is_reviewed=False
            document.save()
            return redirect('subjects',pk1=pk1,pk2=pk2)
    else:
        form = NewDocumentForm()
    return render(request, 'new_document.html', {
        'form': form , 'board': board ,'subject' : subject ,
    })


@login_required
@moderator_required
def review(request, pk1,pk2):
    board = get_object_or_404(Board, pk=pk1)
    subject = get_object_or_404(Subject, pk=pk2)
    documents = Document.objects.all()
    if request.method == 'POST':
        if 'Y' in request.POST:
            i_d=request.POST['Y']
            obj = get_object_or_404(Document,pk=i_d)
            obj.is_reviewed=True
            obj.save()
        elif 'N' in request.POST :
            i_d=request.POST['N']
            obj = get_object_or_404(Document,pk=i_d)
            obj.document.delete(save=True)
            obj.delete()
        return redirect('subjects',pk1=pk1,pk2=pk2)
    else:
        return render(request, 'review.html', {'board': board , 'documents' : documents ,'subject': subject })