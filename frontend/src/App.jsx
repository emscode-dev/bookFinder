import { useState, useRef, useCallback } from 'react'
import './App.css'

const FILTER_OPTIONS = [
  { key: 'all', label: 'All' },
  { key: 'Public Domain', label: 'Public Domain' },
  { key: 'Free Download', label: 'Free Download' },
  { key: 'Read Online', label: 'Read Online' },
  { key: 'Full Preview', label: 'Full Preview' },
  { key: 'Preview', label: 'Preview' },
  { key: 'PDF Available', label: 'PDF' },
  { key: 'EPUB Available', label: 'EPUB' },
]

function App() {
  const [query, setQuery] = useState('')
  const [books, setBooks] = useState([])

  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)
  const [filter, setFilter] = useState('all')
  const [showFilters, setShowFilters] = useState(false)
  const inputRef = useRef(null)

  const search = useCallback(async (q) => {
    const trimmed = q.trim()
    if (!trimmed) return
    setLoading(true)
    setSearched(true)
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(trimmed)}`)
      const data = await res.json()
      setBooks(data.books)
    } catch {
      setBooks([])
    } finally {
      setLoading(false)
    }
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    search(query)
  }

  const filtered = filter === 'all'
    ? books
    : books.filter((b) => b.tags.some((t) => t === filter))

  return (
    <div className="container">
      <form className="searchBar" onSubmit={handleSubmit}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          ref={inputRef}
          type="text"
          placeholder="Search for a book..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" className="searchBtn" disabled={loading || !query.trim()}>
          {loading ? '...' : 'Search'}
        </button>
      </form>

      {searched && !loading && (
        <p className="resultCount">
          {filtered.length} {filtered.length === 1 ? 'result' : 'results'} found
        </p>
      )}

      {loading && (
        <div className="loader">
          <span className="spinner" />
          Searching across sources...
        </div>
      )}

      {!loading && searched && filtered.length === 0 && (
        <div className="empty">
          No results found. Try a different search.
        </div>
      )}

      <div className="resultsList">
        {filtered.map((book) => (
          <div className="card" key={book.id}>
            <div className="cardHeader">
              {book.cover ? (
                <img className="bookImg" src={book.cover} alt={book.title} />
              ) : (
                <div className="bookImg placeholder" />
              )}
              <div className="details">
                <p className="title">{book.title}</p>
                <p className="author">{book.author}</p>
                <div className="tags">
                  {book.tags.map((tag) => (
                    <span className="tag" key={tag}>{tag}</span>
                  ))}
                  {book.year && <span className="tag">{book.year}</span>}
                </div>
              </div>
            </div>
            <div className="cardActions">
              <a href={book.link} target="_blank" rel="noopener noreferrer" className="btnPrimary">
                Read Now
              </a>
              <a href={book.link} target="_blank" rel="noopener noreferrer" className="btnSecondary">
                {book.source}
              </a>
            </div>
          </div>
        ))}
      </div>

      <button className="fab" onClick={() => setShowFilters(!showFilters)}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
        </svg>
        Filters
      </button>

      {showFilters && (
        <div className="filterPanel">
          <div className="filterPanelHeader">
            Filter by access type
            <button className="filterClose" onClick={() => setShowFilters(false)}>&times;</button>
          </div>
          <div className="filterOptions">
            {FILTER_OPTIONS.map((f) => (
              <button
                key={f.key}
                className={`filterChip ${filter === f.key ? 'active' : ''}`}
                onClick={() => { setFilter(f.key); setShowFilters(false) }}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default App
