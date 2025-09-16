# Search Strategies Guide for Markdown Documents

Prefer `ripgrep` (`rg`) - faster and smarter than grep, assume `rg` is available

**Why ripgrep?** 5-10x faster than grep, ignores binary files automatically, respects `.gitignore`, better Unicode support, and cleaner syntax.

## When to Use This Guide

If your initial search returned:
- 🚫 No results when you expect some
- 📚 Too many results to be useful (>50 matches)
- 🎯 Irrelevant or off-topic results
- 🔍 You need to search across different content types (text, code, headings, etc.)

## Search Strategy Escalation

### Level 1: Basic Search
Start here for most queries:

```bash
# Simple case-insensitive search (ripgrep automatically searches recursively)
rg -i "search_term" ./documents/

# Restrict to markdown files only
rg -i --type md "search_term"

# With context (3 lines before/after)
rg -i -C 3 "search_term" --type md
```

**When this fails:** No results or too many results

### Level 2: Flexible Search
Handle variations in terminology:

```bash
# Multiple related terms (OR search)
rg -i "(machine_learning|ML|artificial_intelligence|AI)" --type md

# Word boundaries (avoid partial matches)
rg -i -w "model" --type md

# Allow for different separators
rg -i "(deep.learning|deep_learning|deeplearning)" --type md

# Case-sensitive for acronyms when needed
rg "(API|REST|JSON|HTTP)" --type md
```

**When this fails:** Still no results, need different approach

### Level 3: Structural Search
Search by document structure:

```bash
# Search headings only (lines starting with #)
rg -i "^#{1,6}.*search_term" --type md

# Search code blocks (between triple backticks)
rg -i -A 10 -B 2 "^```.*$" --type md | rg "search_term"

# Search specific heading levels
rg -i "^## .*search_term" --type md

# Search links and references
rg -i "\[.*search_term.*\]" --type md

# Search only in file paths/names
rg -i --files | rg "search_term"
```

**When this fails:** Need to think about synonyms or concepts

### Level 4: Concept Mapping
Break down concepts into components:

```bash
# Instead of "neural networks", try components:
rg -i "(neural|network|neuron|layer|weight|activation)" --type md

# For "machine learning", try:
rg -i "(training|model|algorithm|prediction|classification)" --type md

# For "database", try:
rg -i "(SQL|table|query|index|schema|data)" --type md
```

### Level 5: Advanced Combination Search
Combine multiple strategies:

```bash
# Find documents with multiple related concepts
rg -l -i "python" --type md | xargs rg -l -i "tensorflow" | xargs rg -l -i "model"

# Search with context expansion for related terms
for term in "transformer" "attention" "bert" "gpt"; do
  echo "=== Searching for: $term ==="
  rg -i -C 2 "$term" --type md
done

# Complex regex patterns
rg -i "def\s+\w*train\w*\(" --type md  # Find training function definitions
```

## Search Patterns by Query Type

### Code-Related Queries

```bash
# Function definitions in code blocks
rg -A 10 "^```python" --type md | rg -A 5 -B 5 "def.*function_name"

# Import statements in code blocks
rg -A 20 "^```python" --type md | rg "^import|^from.*import"

# Specific programming concepts
rg -i "(class|function|method|variable|def|import)" --type md

# Code blocks with specific language
rg -A 10 "^```(python|javascript|bash|sql)" --type md

# Find specific error patterns
rg -i "(error|exception|traceback|failed)" --type md
```

### Concept/Theory Queries

```bash
# Academic/technical terms with context
rg -i -C 5 "concept_name" --type md

# With definition indicators
rg -i "(concept.*is|concept.*means|concept.*refers|concept.*defined)" --type md

# In headings (likely definitions)
rg -i "^#.*concept" --type md

# Abstract or introduction sections
rg -i -C 10 "(abstract|introduction|overview)" --type md | rg -i "concept"
```

### How-to/Process Queries

```bash
# Step indicators
rg -i "(step|process|how to|tutorial|guide)" --type md

# Numbered lists
rg "^[0-9]+\." --type md

# Action words with context
rg -i -C 3 "(install|configure|setup|create|build|deploy)" --type md

# Command-line examples
rg -A 5 "^```bash" --type md | rg -i "search_term"
```

## Troubleshooting Failed Searches

### Problem: "No Results Found"

**Possible causes & solutions:**

1. **Typos/Spelling:**
   ```bash
   # Try partial matches with wildcards
   rg -i "machine.*learn" --type md

   # Try common misspellings
   rg -i "(recieve|receive|seperate|separate)" --type md

   # Fuzzy-like search with regex
   rg -i "m[au]ch[iu]ne.*learn[iu]ng" --type md
   ```

2. **Different terminology:**
   ```bash
   # Try synonyms
   rg -i "(AI|artificial intelligence|machine intelligence)" --type md

   # Domain-specific terms
   rg -i "(ML|deep learning|neural net)" --type md
   ```

3. **Hyphenation/spacing variations:**
   ```bash
   # Handle different formats flexibly
   rg -i "(multi.task|multitask|multi_task)" --type md
   rg -i "machine.{0,2}learning" --type md  # 0-2 chars between words
   ```

4. **File type issues:**
   ```bash
   # Check if files are actually markdown
   rg --files --type md

   # Search all text files if markdown filter too restrictive
   rg -i "search_term" --type txt --type md

   # Search without type restriction
   rg -i "search_term" ./documents/
   ```

### Problem: "Too Many Results"

**Refinement strategies:**

1. **Add context constraints:**
   ```bash
   # Combine terms that should appear together
   rg -i "python.*machine.*learning" --type md
   rg -i "machine.*learning" --type md | rg -i "python"
   ```

2. **Focus on document structure:**
   ```bash
   # Only in headings
   rg -i "^#.*search_term" --type md

   # Only in code blocks
   rg -A 20 "^```" --type md | rg -i "search_term"

   # Exclude common sections
   rg -i "search_term" --type md | rg -v -i "(introduction|overview|abstract)"
   ```

3. **Limit by file characteristics:**
   ```bash
   # Only files with specific keywords in filename
   rg --files --type md | rg -i "tutorial|guide" | xargs rg -i "search_term"

   # Recent files only (if file dates matter)
   find ./documents/ -name "*.md" -mtime -30 | xargs rg -i "search_term"
   ```

4. **Use better regex patterns:**
   ```bash
   # Exact phrases
   rg -i "\"machine learning\"" --type md

   # Word boundaries to avoid partial matches
   rg -i -w "train" --type md  # Avoids "training", "constraint"
   ```

### Problem: "Irrelevant Results"

**Focus strategies:**

1. **Use precise regex patterns:**
   ```bash
   # Avoid partial matches
   rg -i -w "apple" --type md  # Won't match "pineapple"

   # Context-sensitive search
   rg -i "apple.*computer|computer.*apple" --type md
   ```

2. **Add required context:**
   ```bash
   # Must appear with related terms nearby
   rg -C 5 -i "train" --type md | rg -i "model|algorithm"

   # Exclude unwanted contexts
   rg -i "apple" --type md | rg -v -i "(fruit|food|eat|recipe)"
   ```

3. **Structure-aware filtering:**
   ```bash
   # Only in specific heading levels
   rg -i "^### .*apple" --type md  # Only level 3 headings

   # Only in code contexts
   rg -A 10 "^```" --type md | rg -i "apple"
   ```

## Advanced Ripgrep Techniques

### File-Level Analysis
```bash
# Get document overviews
rg --files --type md | while read file; do
  echo "=== $file ==="
  rg "^#{1,3}" "$file" | head -5  # Show top-level headings
  echo "Words: $(wc -w < "$file")"
  echo
done

# Find most relevant documents by match count
rg -c -i "search_term" --type md | sort -t: -k2 -nr | head -10

# Show files with context snippets
rg -i "search_term" --type md --max-count 3 -C 2
```

### Cross-Reference Search
```bash
# Find documents mentioning multiple concepts
rg -l -i "concept1" --type md | xargs rg -l -i "concept2"

# Complex relationship searches
rg -i -C 5 "docker" --type md | rg -i "kubernetes" | rg -i "deployment"

# Show co-occurrence patterns
rg -i -C 10 "machine learning" --type md | rg -o -i "\b\w*neural\w*\b" | sort | uniq -c | sort -nr
```

### Pattern Discovery and Analysis
```bash
# Find common patterns around your search term
rg -i -C 3 "search_term" --type md | rg -v "search_term" | sort | uniq -c | sort -nr | head -20

# Extract and analyze heading structure
rg "^#{1,6}" --type md | sed 's/^[^:]*://' | sort | uniq -c | sort -nr

# Find all code languages used
rg "^```\w+" --type md -o | sort | uniq -c | sort -nr

# Analyze linking patterns
rg "\[.*\]\(.*\)" --type md -o | head -20
```

## Ripgrep-Specific Features

### Smart Defaults
```bash
# Ripgrep automatically:
# - Ignores binary files
# - Respects .gitignore
# - Searches recursively by default
# - Uses colored output

# Override defaults when needed:
rg -i "term" --no-ignore          # Include gitignored files
rg -i "term" --hidden             # Include hidden files
rg -i "term" --binary             # Include binary files
rg -i "term" --no-heading         # No file headers in output
```

### Output Control
```bash
# Just filenames
rg -l "search_term" --type md

# Count matches per file
rg -c "search_term" --type md

# Show line numbers
rg -n "search_term" --type md

# Compact output (no empty lines)
rg --compact "search_term" --type md

# Custom output format
rg --replace '$1' '([A-Z][a-z]+)' --type md  # Extract capitalized words
```

### Performance Optimization
```bash
# Limit search depth
rg -i "term" --max-depth 3 --type md

# Limit matches per file
rg -i "term" --max-count 5 --type md

# Use multiple threads (default is optimal)
rg -i "term" --threads 4 --type md

# Memory usage control
rg -i "term" --mmap --type md  # Memory-mapped file I/O
```

## Quick Reference Commands

### Essential Ripgrep Commands
```bash
# Basic search (case-insensitive, markdown only)
rg -i "term" --type md

# With context
rg -i -C 3 "term" --type md

# Multiple terms (OR)
rg -i "(term1|term2)" --type md

# Multiple terms (AND) - files containing both
rg -l "term1" --type md | xargs rg -l "term2"

# Headings only
rg -i "^#.*term" --type md

# Code blocks only
rg -A 10 "^```" --type md | rg -i "term"

# Count matches
rg -c -i "term" --type md

# Just filenames containing term
rg -l -i "term" --type md

# Exact phrase
rg -i "\"exact phrase\"" --type md

# Word boundaries
rg -i -w "word" --type md
```

### File Analysis Commands
```bash
# Find all headings in documents
rg "^#{1,6}" --type md

# Count words in matching files
rg -l "term" --type md | xargs wc -w

# Get document structure
rg "^#{1,3}" document.md

# Find all code blocks by language
rg "^```\w+" --type md

# Show file statistics
rg --files --type md | wc -l  # Count markdown files
```

## When to Escalate to Indexing

Consider creating an index when:
- Regular searches take >5 seconds even with ripgrep
- You frequently search the same large collection (>100MB)
- You need complex boolean queries with scoring
- You want ranked/relevance results
- You need fuzzy/semantic search capabilities
- You're searching across many file types regularly

## Tips for Better Results

1. **Start broad, then narrow** - Ripgrep makes broad searches fast
2. **Use file type restrictions** - `--type md` keeps results relevant
3. **Leverage smart defaults** - Ripgrep ignores what you usually don't want
4. **Combine with standard tools** - `| head`, `| sort`, `| uniq -c` for analysis
5. **Use regex power** - Ripgrep has excellent regex support
6. **Check context** - `-C` flag provides surrounding context
7. **File name patterns** - `--files | rg pattern` for filename searches

## Common Pitfalls to Avoid

❌ **Don't over-specify initially** - Start simple, ripgrep is fast enough
❌ **Don't forget word boundaries** - Use `-w` to avoid partial matches
❌ **Don't ignore file types** - `--type md` saves time and reduces noise
❌ **Don't assume case sensitivity** - Use `-i` for most searches
❌ **Don't forget about regex** - Ripgrep regex is powerful and fast

## Emergency Search Strategy

When nothing else works:
1. Check available markdown files: `rg --files --type md`
2. Sample a few files: `rg "^#{1,2}" random_file.md`
3. Look for overall patterns: `rg "^#" --type md | head -20`
4. Try very broad terms: `rg -i "(the|and|is)" --type md -c | head`
5. Check file extensions: `rg --files | rg "\.(md|txt|doc)$"`
6. Verify search directory: `pwd` and check path
7. Search without restrictions: `rg -i "term" ./`

## Ripgrep vs Grep Cheat Sheet

| Task | grep | ripgrep |
|------|------|---------|
| Basic recursive search | `grep -r "term" .` | `rg "term"` |
| Case insensitive | `grep -ri "term" .` | `rg -i "term"` |
| Specific file types | `grep -r --include="*.md" "term" .` | `rg --type md "term"` |
| Context lines | `grep -r -C 3 "term" .` | `rg -C 3 "term"` |
| Files only | `grep -rl "term" .` | `rg -l "term"` |
| Count matches | `grep -rc "term" .` | `rg -c "term"` |
| Word boundaries | `grep -rw "term" .` | `rg -w "term"` |

Remember: Ripgrep is optimized for speed and developer workflows - use its smart defaults and powerful regex capabilities!
