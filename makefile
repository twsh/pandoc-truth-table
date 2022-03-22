slides.pdf: slides.md truth-table.py
	pandoc --to beamer --output $@ --filter truth-table.py $<

