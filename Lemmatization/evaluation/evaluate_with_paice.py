from nltk.metrics import Paice

lemmas = {'kneel': ['kneel', 'knelt'],
          'range': ['range', 'ranged'],
          'ring': ['ring', 'rang', 'rung']}
stems = {'kneel': ['kneel'],
         'knelt': ['knelt'],
         'rang': ['rang', 'range', 'ranged'],
         'ring': ['ring'],
         'rung': ['rung']}
p = Paice(lemmas, stems)
print(p.gumt, p.gdmt, p.gwmt, p.gdnt)
print(p.errt)
print(p.ui, p.oi, p.sw)
