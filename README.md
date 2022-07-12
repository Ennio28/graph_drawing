# infovis-final-project
Progetto finale per l'esame di [Visualizzazione delle Informazioni](http://www.dia.uniroma3.it/~infovis/) di Roma Tre. Ulteriori informazioni sono disponibili su [Moodle](https://ingegneria.el.uniroma3.it/mod/page/view.php?id=16780), progetto #15.


## Obiettivi
L'obiettivo è esplorare il grafo della [saga islandese Hrafnkels](https://en.wikipedia.org/wiki/Hrafnkels_saga). In particolare si vuole riuscire a comprendere quali siano le relazioni tra i personaggi, definite dalle azioni che li riguardano, studiando il multigrafo a disposizione. 

Il multigrafo diretto contiene nodi con un grado (sia entrante che uscente) molto elevato (anche fino a 20-30 archi uscenti, oltre ad avere archi che partono dallo stesso nodo ed entrano nello stesso nodo.

Il grafo è stato visualizzato mediante l'utilizzo della libreria networkx e plotly in Python utilizzando come algoritmo di disegno del grafo una combinazione di due algoritmi force-directed. Alcuni [esempi](https://plotly.com/python/network-graphs/). Più avanti sono state descritte le soluzioni adottate e le limitazioni presenti, insieme ai possibili sviluppi futuri.



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
- ```drawing_2D()```: per disegnare il grafo in 2D.
- ```drawing_3D()```: per disegnare il grafo in 3D, in maniera tale che ci si possa interagire.
- ```drawing_2D_interactive```: per disegnare il grafo in 2D, in maniera tale che ci si possa interagire.

### ```drawing_2D()```
Con questo metodo si ottiene una rappresentazione statica del grafo. Sono stati riportati tutti i nodi ed i vertici del grafo rappresentati dal dataset. La principale limitazione_di questo metodo 
è dovuta dall'impossibilità di rappresentare le label dei multiarchi. Ciò non è possibile poiché la libreria networkx, di Python, non prevede questa feature.
Inoltre non si può interagire con la figura, per cui si consiglia di usare il metodo ```drawing_2D_interactive```.

### ```drawing_3D()```
Ho iniziato a programmare questa funzione in modo tale che l'utente finale potesse interagire con il grafo in una maniera più immersiva, ma avendo tanti nodi e tanti archi la sua visualizzazione risultava confusa. 
Ho scelto per questo motivo di non rappresentare le label degli archi e dei nodi, in maniera tale da poter vedere la struttura del grafo in 3D. Ad ogni modo si consiglia di utilizzare la funzione  ```drawing_2D_interactive```.
## Sviluppi Futuri
Lo sfruttamento della componente temporale potrebbe essere fondamentale per visualizzare bene questo grafo, usando come informazione il capitolo dei personaggi e delle azioni (il numero di pagina è mancante troppo spesso). Questa soluzione consente di visualizzare un sottoinsieme di nodi e archi alla volta, e di analizzare la storia seguendo una linea temporale causale, il che consentirebbe una comprensione sicuramente migliore. Un [esempio](https://observablehq.com/@d3/temporal-force-directed-graph) D3.js implementa tale funzionalità.

L'utilizzo di [forze](https://www.d3indepth.com/force-layout/#forcex-and-forcey) come ```forceX``` e ```forceY``` può essere molto utile per posizionare i nodi in una configurazione migliore, senza dover gestire il tweaking delle forze già definite (che non è sempre triviale). Tuttavia ciò richiederebbe di definire nuovi campi nel dataset che specifichino posizioni x e y per ogni nodo.

Per gestire meglio le label degli archi (che a volte sono poco leggibili per nodi con grado elevato) si potrebbe visualizzare la lista di azioni in una finestra popup che viene mostrata solo quando si fa hovering del mouse sul nodo/arco di interesse, vedere [esempio](https://bl.ocks.org/almsuarez/fa9502b0087b829ef4d97e5d6d5ccfde). In questo modo non si avrebbe più necessità di visualizzare testo contemporaneamente, ma solo dove l'utente lo richiede, migliorando la leggibilità.

Un'altra soluzione per gestire i numerosi archi e label è quella di compattarli in un unico arco, e gestire la lista di azioni risultante con delle icone. Queste icone saranno diverse per ogni azione del dataset, e verranno visualizzate in punti diversi dell'arco evitando sovrapposizione. Inoltre è necessario selezionare i nodi con azioni onclick, per poter poi fare hovering sulle icone per avere una descrizione dell'azione (o usare una legenda). Per fare rendering di immagini png sugli archi vedere questo [esempio](https://stackoverflow.com/questions/32143614/force-directed-graph-how-to-add-icon-in-the-middle-of-an-edge). Inoltre sono state già scaricate delle icone per una possibile implementazione di questa funzionalità, [qui](https://github.com/ale-pavel/infovis-final-project/tree/feature/icons-labels/icons) disponibili (branch feature/icons-labels).

Un possibile modo di gestire la densità dei nodi è mediante una forza repulsiva, attivata quando si fa click su un nodo (che rimane fermo). In questo [esempio](https://observablehq.com/@d3/collision-detection/2?collection=@d3/d3-force) l'hovering del mouse sposta i diversi nodi.
