# 📚 Universal Free & Accessible Book Finder

**Universal Book Finder** is an open-source web application designed to help readers navigate the fragmented world of digital literature. 

Instead of hosting copyrighted files, this project serves as a **centralized aggregator and search engine**. Users can search for a specific book title and instantly discover the legal avenues available to read it—whether that means downloading a public domain EPUB, borrowing from a local library via API, or reading a preview.

## 🎯 The Mission
The internet is full of information, but finding a specific book legally can be a nightmare. We aim to solve the "Where can I read this?" problem by checking multiple legitimate sources simultaneously.

**We do not host or store book PDFs.** We simply connect readers to the platforms that do.

## ✨ How It Works
1. **Search:** A user enters a book title or author.
2. **Aggregate:** The system queries multiple supported APIs (Open Library, Project Gutenberg, Internet Archive, etc.).
3. **Filter:** Results are categorized by access type (Public Domain, Borrowable, Preview, Purchasable).
4. **Redirect:** The user is sent to the source to consume the content legally.

## 🚀 Features (Roadmap)
- [ ] **Multi-Source Search:** Query multiple APIs in parallel for the fastest results.
- [ ] **Access Filtering:** Filter by "Read Online," "Download," "Borrow," or "Buy."
- [ ] **Open Library Integration:** Pull metadata (covers, ISBN, descriptions) from Open Library.
- [ ] **Public Domain Focus:** Highlight free, unrestricted works (Gutenberg, Standard Ebooks).
- [ ] **Local Library Locator:** (Future) Use geolocation to find the book in the user's physical local library system.
- [ ] **No Paywalls:** Strictly a discovery tool for free and legal access.

## 🛠️ Tech Stack (Planned)
- **Frontend:** React / Next.js / Tailwind CSS
- **Backend:** Node.js / Python (FastAPI)
- **APIs:** Open Library API, Project Gutenberg, Internet Archive, Google Books API.
- **Database:** (Optional) Redis for caching search results to reduce API latency.

## 🤝 Contributing
We welcome contributions from developers, designers, and book lovers! Whether you want to add a new source API or improve the UI, please check out our `CONTRIBUTING.md`.

## ⚖️ Legal Disclaimer
This project is a search aggregator. It does not host, upload, or distribute copyrighted material. All links provided direct users to legitimate third-party services (e.g., library systems, public domain archives, or official retailer previews). We strictly oppose digital piracy.