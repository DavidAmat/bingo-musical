# Makefile for Bingo Musical Card Generation
# Variables
PYTHON = python3
TITLE = "Bingo musical LA SIRENA"
BG_COLOR = "\#FFEAB3"
IMAGES = images/hat.png images/notes.png
COUNT = 30
SEED = 42

# Directories
OUTPUT_CARDS = output/cards
OUTPUT_SHEETS = output/sheets
OUTPUT_PDF = output/sheets/pdf

# Default target
.PHONY: all
all: generate pdf

# Generate all HTML cards and sheets
.PHONY: generate
generate:
	@echo "Generating bingo cards and sheets..."
	$(PYTHON) generate_bingo.py --title $(TITLE) --bg $(BG_COLOR) --images $(IMAGES) --count $(COUNT) --seed $(SEED)
	@echo "✓ Cards and sheets generated!"

# Convert all sheets to PDF
.PHONY: pdf
pdf:
	@echo "Converting sheets to PDF..."
	$(PYTHON) convert_to_pdf.py $(OUTPUT_SHEETS) --glob "sheet_*.html" --outdir $(OUTPUT_PDF)
	@echo "✓ PDFs created!"

# Run everything
.PHONY: run
run: all

# Generate a single test card
.PHONY: test
test:
	@echo "Generating test card..."
	$(PYTHON) bingo_card_test.py
	@echo "✓ Test card created at test_card.html"

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	rm -rf $(OUTPUT_CARDS)/*.html
	rm -rf $(OUTPUT_SHEETS)/*.html
	rm -rf $(OUTPUT_PDF)/*.pdf
	rm -f test_card.html
	@echo "✓ Cleaned!"

# Clean and regenerate everything
.PHONY: rebuild
rebuild: clean all

# Show help
.PHONY: help
help:
	@echo "Bingo Musical Card Generator - Available commands:"
	@echo ""
	@echo "  make            - Generate cards, sheets, and PDFs (default)"
	@echo "  make all        - Same as 'make'"
	@echo "  make generate   - Generate HTML cards and sheets only"
	@echo "  make pdf        - Convert sheets to PDF only"
	@echo "  make test       - Generate a single test card"
	@echo "  make clean      - Remove all generated files"
	@echo "  make rebuild    - Clean and regenerate everything"
	@echo "  make help       - Show this help message"
	@echo ""
	@echo "Configuration:"
	@echo "  TITLE    = $(TITLE)"
	@echo "  BG_COLOR = $(BG_COLOR)"
	@echo "  COUNT    = $(COUNT)"
	@echo "  SEED     = $(SEED)"

