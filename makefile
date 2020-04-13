TEX=xelatex
BIBTEX=bibtex

FILE=171860013_3月报告
.PHONY: default, clean

default:
	$(TEX) $(FILE).tex
	$(BIBTEX) $(FILE)
	$(TEX) $(FILE).tex
	$(TEX) $(FILE).tex

clean:
	-rm -f *.blg *.bbl *.log *.aux *.out *.spl comment.cut *.synctex.gz
	-rm -f $(FILE).pdf
