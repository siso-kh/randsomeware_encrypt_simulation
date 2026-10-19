/* Bookstore Inventory - frontend logic.
   Fetches the catalog from the API server (file111.py, port 8000 per
   folder2/folder21/file211.ini) and renders rows into file121.html. */

const API_BASE = "http://localhost:8000";

async function fetchBooks() {
  const response = await fetch(`${API_BASE}/api/books`);
  if (!response.ok) {
    throw new Error(`API returned ${response.status}`);
  }
  const data = await response.json();
  return data.books;
}

function renderBookRow(book) {
  const tr = document.createElement("tr");

  const stockCell = book.stock > 0 ? `${book.stock} in stock` : "Out of stock";
  const button = book.stock > 0
    ? `<button data-book-id="${book.id}">Order</button>`
    : `<button disabled>Unavailable</button>`;

  tr.innerHTML = `
    <td>${book.title}</td>
    <td>${book.author}</td>
    <td>$${book.price.toFixed(2)}</td>
    <td class="${book.stock > 0 ? "in-stock" : "out-of-stock"}">${stockCell}</td>
    <td>${button}</td>`;

  return tr;
}

function attachOrderHandler(button, book) {
  button.addEventListener("click", async () => {
    const response = await fetch(`${API_BASE}/api/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ book_id: book.id, quantity: 1 }),
    });
    if (response.ok) {
      const order = await response.json();
      alert(`Order confirmed: ${book.title} for $${order.total.toFixed(2)}`);
      loadCatalog(); // refresh stock counts
    } else {
      const error = await response.json();
      alert(`Order failed: ${error.detail}`);
    }
  });
}

async function loadCatalog() {
  const status = document.getElementById("status");
  const tbody = document.querySelector("#book-table tbody");
  tbody.innerHTML = "";

  try {
    const books = await fetchBooks();
    status.textContent = `${books.length} titles available`;
    for (const book of books) {
      const row = renderBookRow(book);
      const button = row.querySelector("button");
      if (!button.disabled) attachOrderHandler(button, book);
      tbody.appendChild(row);
    }
  } catch (err) {
    status.textContent = `Could not load catalog: ${err.message}`;
    console.error(err);
  }
}

document.addEventListener("DOMContentLoaded", loadCatalog);
