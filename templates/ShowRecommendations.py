from browser import document,console,alert

exec(open('evaluator.py').read())

def show(e):
    console.log('Hello')
    alert('Hello World')
    document['hello'] <='Yoooo'

document['alert-btn'].bind('click',show)