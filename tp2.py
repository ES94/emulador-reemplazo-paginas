"""
TP 2 - Algoritmos de Reemplazo

Integrantes:
    Mauricio Rosso <maurirosso@hotmail.com>
    Antonela Orellano <anto_orellano09@hotmail.com>
    Emanuel Stradella <e.stradella94@outlook.com>
"""

import doctest


def print_estado(memoria, fallo, marcas=None, puntero=None):
    """Imprime el estado de la memoria"""
    if marcas is not None:
        print("-" * 10)
        print("[%s]" % ', '.join(['*' if n else ' ' for n in marcas]))
    print("[%s]%s" % (', '.join([str(p) if p is not None else ' ' for p in memoria]),
                      ' F' if fallo else ''))
    if puntero is not None:
        print("[%s]" % ', '.join(['|' if n == puntero else ' ' for n in range(len(memoria))]))


def optimo(memoria, paginas):
    """Optimo

    >>> optimo([None, None, None, None], [1, 2, 3, 4, 5, 6, 7, 8])
    [1,  ,  ,  ]
    [1, 2,  ,  ]
    [1, 2, 3,  ]
    [1, 2, 3, 4]
    [5, 2, 3, 4] F
    [5, 6, 3, 4] F
    [5, 6, 7, 4] F
    [5, 6, 7, 8] F

    >>> optimo([None, None, None], [1, 2, 3, 1, 4, 1, 5, 2, 1])
    [1,  ,  ]
    [1, 2,  ]
    [1, 2, 3]
    [1, 2, 3]
    [1, 2, 4] F
    [1, 2, 4]
    [1, 2, 5] F
    [1, 2, 5]
    [1, 2, 5]

    >>> optimo([None, None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4])
    [1,  ,  ,  ]
    [1, 2,  ,  ]
    [1, 2,  ,  ]
    [1, 2, 3,  ]
    [1, 2, 3, 4]
    [1, 2, 5, 4] F
    [1, 2, 5, 4]
    [1, 2, 5, 4]
    [1, 2, 5, 4]
    [1, 2, 5, 4]

    >>> optimo([None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4, 6, 7, 6, 1])
    [1,  ,  ]
    [1, 2,  ]
    [1, 2,  ]
    [1, 2, 3]
    [1, 2, 4] F
    [1, 2, 5] F
    [1, 2, 5]
    [1, 2, 5]
    [1, 2, 5]
    [1, 4, 5] F
    [1, 4, 6] F
    [1, 7, 6] F
    [1, 7, 6]
    [1, 7, 6]
    """

    counter = 0
    pagesQueue = [] # Cola de págs: ordena las págs. en memoria según su
                    # antiguedad, para ser usada en la selección FIFO.

    for pagina in paginas:
        fallo = False
        counter += 1
        victim = None
        victimIndex = -1
        nonRefPages = 0

        if pagina not in memoria:
            if None in memoria:
                for frame in memoria:
                    if frame == None:
                        victimIndex = memoria.index(frame)
                        pagesQueue.insert(0, pagina)
                        break
            else:
                fallo = True
            
                for page in memoria:
                    if page not in paginas[counter:]:
                        nonRefPages += 1

                if nonRefPages > 1:
                    nonRefPages = 0
                    
                    for page in memoria:
                        if page not in paginas[counter:]:
                            nonRefPages += 1

                            if nonRefPages == 1:
                                victim = page
                                victimIndex = memoria.index(page)
                            elif pagesQueue.index(page) > pagesQueue.index(victim):
                                victim = page
                                victimIndex= memoria.index(page)
                else:
                    for page in memoria:
                        if page in paginas[counter:]:
                            if memoria.index(page) == 0:
                                victim = page
                                victimIndex = memoria.index(page)
                            elif paginas[counter:].index(page) > paginas[counter:].index(victim):
                                victim = page
                                victimIndex = memoria.index(page)
                        else:
                            victim = page
                            victimIndex = memoria.index(page)
                            break

                pagesQueue.remove(victim)
                pagesQueue.insert(0, pagina)
                    
            memoria[victimIndex] = pagina
        else:
            pagesQueue.remove(pagina)
            pagesQueue.insert(0, pagina)
            
        print_estado(memoria, fallo)


def fifo(memoria, paginas):
    """FIFO

    >>> fifo([None, None, None, None], [1, 2, 3, 4, 5, 6, 7, 8])
    [1,  ,  ,  ]
    [1, 2,  ,  ]
    [1, 2, 3,  ]
    [1, 2, 3, 4]
    [5, 2, 3, 4] F
    [5, 6, 3, 4] F
    [5, 6, 7, 4] F
    [5, 6, 7, 8] F

    >>> fifo([None, None, None], [1, 2, 3, 1, 4, 1, 5, 2, 1])
    [1,  ,  ]
    [1, 2,  ]
    [1, 2, 3]
    [1, 2, 3]
    [4, 2, 3] F
    [4, 1, 3] F
    [4, 1, 5] F
    [2, 1, 5] F
    [2, 1, 5]

    >>> fifo([None, None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4])
    [1,  ,  ,  ]
    [1, 2,  ,  ]
    [1, 2,  ,  ]
    [1, 2, 3,  ]
    [1, 2, 3, 4]
    [5, 2, 3, 4] F
    [5, 2, 3, 4]
    [5, 1, 3, 4] F
    [5, 1, 2, 4] F
    [5, 1, 2, 4]

    >>> fifo([None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4, 6, 7, 6, 1])
    [1,  ,  ]
    [1, 2,  ]
    [1, 2,  ]
    [1, 2, 3]
    [4, 2, 3] F
    [4, 5, 3] F
    [4, 5, 2] F
    [1, 5, 2] F
    [1, 5, 2]
    [1, 4, 2] F
    [1, 4, 6] F
    [7, 4, 6] F
    [7, 4, 6]
    [7, 1, 6] F
    """

    Puntero = 0

    for pagina in paginas:
        fallo = False
        SeInserto = False
        PagRepetida = False
        
        for mem in range(0, len(memoria)):
            if memoria[mem] == None:
                for m in memoria:
                    if m == pagina:
                        PagRepetida = True
                        break
                if PagRepetida == False:
                    memoria[mem] = pagina
                    SeInserto = True
                    break
                               
        if SeInserto == False:
            for mem in range(0, len(memoria)):
                if pagina == memoria[mem]:
                    PagRepetida = True
                    
            if PagRepetida == False:        
                if Puntero > (len(memoria) - 1):
                        Puntero = 0
                memoria[Puntero] = pagina
                Puntero += 1
                    
                fallo = True
        print_estado(memoria, fallo)


def lru(memoria, paginas):
    """LRU

    >>> lru([None, None, None, None], [1, 2, 3, 4, 5, 6, 7, 8])
    [1,  ,  ,  ]
    [1, 2,  ,  ]
    [1, 2, 3,  ]
    [1, 2, 3, 4]
    [5, 2, 3, 4] F
    [5, 6, 3, 4] F
    [5, 6, 7, 4] F
    [5, 6, 7, 8] F

    >>> lru([None, None, None], [1, 2, 3, 1, 4, 1, 5, 2, 1])
    [1,  ,  ]
    [1, 2,  ]
    [1, 2, 3]
    [1, 2, 3]
    [1, 4, 3] F
    [1, 4, 3]
    [1, 4, 5] F
    [1, 2, 5] F
    [1, 2, 5]

    >>> lru([None, None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4])
    [1,  ,  ,  ]
    [1, 2,  ,  ]
    [1, 2,  ,  ]
    [1, 2, 3,  ]
    [1, 2, 3, 4]
    [1, 5, 3, 4] F
    [2, 5, 3, 4] F
    [2, 5, 1, 4] F
    [2, 5, 1, 4]
    [2, 5, 1, 4]

    >>> lru([None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4, 6, 7, 6, 1])
    [1,  ,  ]
    [1, 2,  ]
    [1, 2,  ]
    [1, 2, 3]
    [1, 4, 3] F
    [5, 4, 3] F
    [5, 4, 2] F
    [5, 1, 2] F
    [5, 1, 2]
    [4, 1, 2] F
    [4, 6, 2] F
    [4, 6, 7] F
    [4, 6, 7]
    [1, 6, 7] F
    """

    counter = -1
    pagesQueue = [] # Cola de págs: ordena las págs. en memoria según su
                    # antiguedad, para ser usada en la selección FIFO.

    for pagina in paginas:
        fallo = False
        counter += 1 # Lleva la cuenta de las págs. entrantes. Es también el
                     # índice de la pág. actual.
        victim = None
        victimIndex = -1
        nonRefPages = 0

        if pagina not in memoria:
            if None in memoria:
                for frame in memoria:
                    if frame == None:
                        victimIndex = memoria.index(frame)
                        pagesQueue.insert(0, pagina)
                        break
            else:
                fallo = True
                victim = pagesQueue[len(pagesQueue) - 1]
                victimIndex = memoria.index(victim)
                pagesQueue.remove(victim)
                pagesQueue.insert(0, pagina)
                    
            memoria[victimIndex] = pagina
        else:
            pagesQueue.remove(pagina)
            pagesQueue.insert(0, pagina)
        
        print_estado(memoria, fallo)


def reloj(memoria, paginas):
    """Reloj

    >>> reloj([None, None, None, None], [1, 2, 3, 4, 5, 6, 7, 8])
    ----------
    [ ,  ,  ,  ]
    [1,  ,  ,  ]
    [ , |,  ,  ]
    ----------
    [ ,  ,  ,  ]
    [1, 2,  ,  ]
    [ ,  , |,  ]
    ----------
    [ ,  ,  ,  ]
    [1, 2, 3,  ]
    [ ,  ,  , |]
    ----------
    [ ,  ,  ,  ]
    [1, 2, 3, 4]
    [|,  ,  ,  ]
    ----------
    [ ,  ,  ,  ]
    [5, 2, 3, 4] F
    [ , |,  ,  ]
    ----------
    [ ,  ,  ,  ]
    [5, 6, 3, 4] F
    [ ,  , |,  ]
    ----------
    [ ,  ,  ,  ]
    [5, 6, 7, 4] F
    [ ,  ,  , |]
    ----------
    [ ,  ,  ,  ]
    [5, 6, 7, 8] F
    [|,  ,  ,  ]

    >>> reloj([None, None, None], [1, 2, 3, 1, 4, 1, 5, 2, 1])
    ----------
    [ ,  ,  ]
    [1,  ,  ]
    [ , |,  ]
    ----------
    [ ,  ,  ]
    [1, 2,  ]
    [ ,  , |]
    ----------
    [ ,  ,  ]
    [1, 2, 3]
    [|,  ,  ]
    ----------
    [*,  ,  ]
    [1, 2, 3]
    [|,  ,  ]
    ----------
    [ ,  ,  ]
    [1, 4, 3] F
    [ ,  , |]
    ----------
    [*,  ,  ]
    [1, 4, 3]
    [ ,  , |]
    ----------
    [*,  ,  ]
    [1, 4, 5] F
    [|,  ,  ]
    ----------
    [ ,  ,  ]
    [1, 2, 5] F
    [ ,  , |]
    ----------
    [*,  ,  ]
    [1, 2, 5]
    [ ,  , |]

    >>> reloj([None, None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4])
    ----------
    [ ,  ,  ,  ]
    [1,  ,  ,  ]
    [ , |,  ,  ]
    ----------
    [ ,  ,  ,  ]
    [1, 2,  ,  ]
    [ ,  , |,  ]
    ----------
    [*,  ,  ,  ]
    [1, 2,  ,  ]
    [ ,  , |,  ]
    ----------
    [*,  ,  ,  ]
    [1, 2, 3,  ]
    [ ,  ,  , |]
    ----------
    [*,  ,  ,  ]
    [1, 2, 3, 4]
    [|,  ,  ,  ]
    ----------
    [ ,  ,  ,  ]
    [1, 5, 3, 4] F
    [ ,  , |,  ]
    ----------
    [ ,  ,  ,  ]
    [1, 5, 2, 4] F
    [ ,  ,  , |]
    ----------
    [*,  ,  ,  ]
    [1, 5, 2, 4]
    [ ,  ,  , |]
    ----------
    [*,  , *,  ]
    [1, 5, 2, 4]
    [ ,  ,  , |]
    ----------
    [*,  , *, *]
    [1, 5, 2, 4]
    [ ,  ,  , |]

    >>> reloj([None, None, None], [1, 2, 1, 3, 4, 5, 2, 1, 2, 4, 6, 7, 6, 1])
    ----------
    [ ,  ,  ]
    [1,  ,  ]
    [ , |,  ]
    ----------
    [ ,  ,  ]
    [1, 2,  ]
    [ ,  , |]
    ----------
    [*,  ,  ]
    [1, 2,  ]
    [ ,  , |]
    ----------
    [*,  ,  ]
    [1, 2, 3]
    [|,  ,  ]
    ----------
    [ ,  ,  ]
    [1, 4, 3] F
    [ ,  , |]
    ----------
    [ ,  ,  ]
    [1, 4, 5] F
    [|,  ,  ]
    ----------
    [ ,  ,  ]
    [2, 4, 5] F
    [ , |,  ]
    ----------
    [ ,  ,  ]
    [2, 1, 5] F
    [ ,  , |]
    ----------
    [*,  ,  ]
    [2, 1, 5]
    [ ,  , |]
    ----------
    [*,  ,  ]
    [2, 1, 4] F
    [|,  ,  ]
    ----------
    [ ,  ,  ]
    [2, 6, 4] F
    [ ,  , |]
    ----------
    [ ,  ,  ]
    [2, 6, 7] F
    [|,  ,  ]
    ----------
    [ , *,  ]
    [2, 6, 7]
    [|,  ,  ]
    ----------
    [ , *,  ]
    [1, 6, 7] F
    [ , |,  ]
    """

    puntero = 0
    marcas = [0 for n in [n for n in memoria]]

    for pagina in paginas:
        fallo = False

        if pagina not in memoria:
            if None in memoria:
                memoria[puntero] = pagina
            else:
                fallo = True

                while True:
                    if marcas[puntero] == 1:
                        marcas[puntero] = 0
                    else:
                        memoria[puntero] = pagina
                        break

                    puntero += 1

                    if puntero > len(memoria) - 1:
                        puntero = 0

            puntero += 1

            if puntero > len(memoria) - 1:
                puntero = 0
        else:
            marcas[memoria.index(pagina)] = 1
                            
        print_estado(memoria, fallo, marcas, puntero)


if __name__ == "__main__":
    doctest.testmod(verbose=True)
