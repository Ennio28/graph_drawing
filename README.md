# infovis-final-project
Progetto finale per l'esame di [Visualizzazione delle Informazioni](http://www.dia.uniroma3.it/~infovis/) di Roma Tre. Ulteriori informazioni sono disponibili su [Moodle](https://ingegneria.el.uniroma3.it/mod/page/view.php?id=16780), progetto #15.


## Obiettivi
<br/>L'obiettivo è esplorare il grafo della [saga islandese Hrafnkels](https://en.wikipedia.org/wiki/Hrafnkels_saga). In particolare si vuole riuscire a comprendere quali siano le relazioni tra i personaggi, definite dalle azioni che li riguardano, studiando il multigrafo a disposizione. 

Il multigrafo diretto contiene nodi con un grado (sia entrante che uscente) molto elevato (anche fino a 20-30 archi uscenti, oltre ad avere archi che partono dallo stesso nodo ed entrano nello stesso nodo.

Il grafo è stato visualizzato mediante l'utilizzo della libreria networkx e plotly in Python utilizzando come algoritmo di disegno del grafo una combinazione di due algoritmi force-directed. Alcuni [esempi](https://plotly.com/python/network-graphs/). Più avanti sono state descritte le soluzioni adottate e le limitazioni presenti, insieme ai possibili sviluppi futuri.<br/>


## Tecnologie e Librerie usate
Per il disegno del grafo:
- `Python`
- `matplotlib.pyplot`
- `networkx`
- `plotly`

Per l'elaborazione del dataset le librerie  :
- `json`
- `csv`


## Dataset
Il [dataset](https://github.com/Ennio28/graph_drawing/blob/master/hrafnkel_saga_network.xlsx) contiene le seguenti informazioni:

- Nodi (rappresentano i personaggi)
    - ```id```: codice identificativo (43 in tutto)
    - ```label```: nome del personaggio
    - ```gender```: genere del personaggio (vedere dataset)
    - ```chapter```: il capitolo in cui il personaggio appare per la prima volta
    - ```page```: la pagina in cui è menzionato per la prima volta
- Archi (rappresentano azioni tra personaggi)
    - ```source```: id del personaggio da cui parte l'azione
    - ```target```: id del secondo personaggio
    - ```action```: codice dell'azione (28 in tutto, vedere dataset)
    - ```chapter```: il capitolo in cui l'azione è descritta
    - ```page```: la pagina in cui accade


## Soluzioni adottate

Per gestire il disegno del grafo sono state usati diversi approcci, in particolare si riportano i seguenti metodi:
- ```drawing_2D()```:  <br/>per disegnare il grafo in 2D. <br/>
- ```drawing_3D()```:  <br/>per disegnare il grafo in 3D, in maniera tale che ci si possa interagire. <br/>
- ```drawing_2D_interactive```:  <br/>per disegnare il grafo in 2D, in maniera tale che ci si possa interagire. <br/>

## ```drawing_2D()```
 <br/>Con questo metodo si ottiene una rappresentazione statica del grafo. Sono stati riportati tutti i nodi e i vertici del grafo rappresentati dal dataset. La principale limitazione di questo metodo 
è dovuta dall'impossibilità di rappresentare le label dei multiarchi. Ciò non è possibile poiché la libreria networkx, di Python, non prevede questa feature per archi multipli.
Inoltre non si può interagire con la figura,al di fuori dello zoom, per cui si consiglia di usare il metodo ```drawing_2D_interactive```. <br/>

## ```drawing_3D()```
 <br/>Ho iniziato a programmare questa funzione in modo tale che l'utente finale potesse interagire con il grafo in una maniera più immersiva, ma avendo tanti nodi e tanti archi la sua visualizzazione risultava confusa. 
Ho scelto per questo motivo di non rappresentare le label degli archi e dei nodi, in maniera tale da poter vedere la struttura del grafo in 3D.Inoltre,
 per questo motivo, ho rappresentato un numero ridotto di archi. Gli archi rappresentati, infatti, sono solo quelli relativi ad azioni differenti<br/>
 <br/>Ad ogni modo si consiglia di utilizzare la funzione  ```drawing_2D_interactive```. <br/>



## ```drawing_2D_interactive```
<br/>Per il disegno del grafo, in questo metodo, ho utilizzato le librerie [networkx](https://networkx.org/documentation/stable/reference/drawing.html) e [plotly](https://plotly.com/python-api-reference/) 
Come per gli altri metodi i nodi sono stati colorati in maniera differente a seconda del genere dei personaggi. Infatti, nel dataset i personaggi hanno tre possibili tipi di genere: _maschi_, _femmine_ e _neutri_. Per cui la scelta 
del colore è ricaduta sui colori blu, rosa e verde rispettivamente. Sono stati scelti questi colori, per lo meno i primi due, perché di norma si usano questi colori per rappresentare il genere di una persona. Per il disegno del grafo ho usato<br/>
tre metodi della libreria `networkx`:<br/>

- [spiral_layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spiral_layout.html)
- [kamada_kawai_layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.kamada_kawai_layout.html)
- [spring_layout](https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html)


<br/>L'output dei metodi, delle librerie, è stato passato come punto di partenza per il successivo. Sono stati scelti, e messi in quest'ordine, dopo un test di preferenza su un piccolo numero di utenti.<br/>

<br/>È possibile fare panning e zoom sull'interfaccia grazie all'utilizzo della libreria Plotly. Inoltre per permettere di fruire meglio della visualizzazione le label dei nodi sono visualizzate sempre
e facendo hovering con il mouse vengono ulteriormente mostrate.
<br/>

## Sviluppi Futuri
<br/>Si potrebbe sfruttare la componente temporale per visualizzare il grafo in maniera più appropriata. 
Usando degli sliders si consentirebbe di visualizzare un sottoinsieme di nodi ed archi seguendo la narrazione della storia.
Infatti si potrebbero mostrare i nodi e gli archi, sfruttando la variabile relativa alle pagine. Questo tipo di approccio consente di analizzare la Saga seguendone la linea temporale della storia.<br/>

