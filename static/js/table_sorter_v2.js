document.addEventListener("DOMContentLoaded", function() {
    // Inject CSS for table sorting indicators
    const style = document.createElement('style');
    style.textContent = `
        th.sortable-header {
            cursor: pointer !important;
            user-select: none !important;
            position: relative;
            padding-right: 24px !important;
            transition: background-color 0.2s ease;
        }
        th.sortable-header:hover {
            background-color: rgba(0, 0, 0, 0.05) !important;
        }
        .sort-arrow {
            position: absolute;
            right: 8px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 10px;
            color: #94a3b8;
            opacity: 0.6;
        }
        th.sort-asc .sort-arrow, th.sort-desc .sort-arrow {
            color: #0b57c6;
            opacity: 1;
        }
    `;
    document.head.appendChild(style);

    const tables = document.querySelectorAll("table");
    tables.forEach(table => {
        const headers = table.querySelectorAll("thead th");
        const tbody = table.querySelector("tbody");
        if (!tbody) return;

        const originalRows = Array.from(tbody.querySelectorAll("tr"));
        const isEmpty = originalRows.length === 0 || 
                        (originalRows.length === 1 && 
                         (originalRows[0].querySelector('td[colspan]') || 
                          originalRows[0].textContent.toLowerCase().includes("tidak ada") || 
                          originalRows[0].textContent.toLowerCase().includes("kosong")));
        if (isEmpty) return;

        let currentRows = [...originalRows];

        // Find "No" column index to update numbers after sorting
        let noColIndex = -1;
        headers.forEach((header, index) => {
            const text = header.textContent.trim().toUpperCase();
            if (text === "NO" || text === "NO." || text === "#") {
                noColIndex = index;
            }
        });

        // Add sorting functionality
        headers.forEach((header, index) => {
            const headerText = header.textContent.trim().toUpperCase();

            // Skip non-sortable columns (like No, Action, etc.)
            if (headerText === "NO" || headerText === "NO." || headerText === "AKSI" || headerText === "ACTION" || 
                headerText === "DETAIL" || headerText === "DETIL" || headerText === "" ||
                header.querySelector("input[type='checkbox']")) {
                return;
            }

            header.classList.add("sortable-header");
            header.title = "Klik untuk mengurutkan";

            const oldArrow = header.querySelector(".sort-arrow");
            if (oldArrow) oldArrow.remove();

            const arrowSpan = document.createElement("span");
            arrowSpan.className = "sort-arrow";
            arrowSpan.innerHTML = "↕";
            header.appendChild(arrowSpan);

            let asc = true;

            header.addEventListener("click", () => {
                headers.forEach(h => {
                    if (h !== header) {
                        h.classList.remove("sort-asc", "sort-desc");
                        const otherArrow = h.querySelector(".sort-arrow");
                        if (otherArrow) {
                            otherArrow.innerHTML = "↕";
                        }
                    }
                });

                currentRows.sort((rowA, rowB) => {
                    if (rowA.children.length <= index || rowB.children.length <= index) return 0;

                    const cellA = rowA.children[index].textContent.trim();
                    const cellB = rowB.children[index].textContent.trim();

                    const cleanValue = (val) => {
                        let cleaned = val.replace(/Rp\.?\s*/gi, '')
                                         .replace(/\.?\d+k/gi, '')
                                         .replace(/gb|tb|kg|inch|"/gi, '')
                                         .replace(/\./g, '')
                                         .replace(/,/g, '.')
                                         .trim();

                        if (!isNaN(cleaned) && cleaned !== "") {
                            return parseFloat(cleaned);
                        }

                        const dateMatch = val.match(/^(\d{1,2})[\s/-]([a-zA-Z]+|\d{1,2})[\s/-](\d{4})/);
                        if (dateMatch) {
                            const dateParsed = Date.parse(val);
                            if (!isNaN(dateParsed)) return dateParsed;
                        }

                        return val.toLowerCase();
                    };

                    const valA = cleanValue(cellA);
                    const valB = cleanValue(cellB);

                    if (typeof valA === "number" && typeof valB === "number") {
                        return asc ? valA - valB : valB - valA;
                    }

                    return asc 
                        ? valA.toString().localeCompare(valB.toString(), undefined, {numeric: true, sensitivity: 'base'})
                        : valB.toString().localeCompare(valA.toString(), undefined, {numeric: true, sensitivity: 'base'});
                });

                if (asc) {
                    header.classList.remove("sort-desc");
                    header.classList.add("sort-asc");
                    arrowSpan.innerHTML = "▲";
                } else {
                    header.classList.remove("sort-asc");
                    header.classList.add("sort-desc");
                    arrowSpan.innerHTML = "▼";
                }

                asc = !asc;

                // Re-append sorted rows to tbody
                tbody.innerHTML = '';
                currentRows.forEach(row => {
                    tbody.appendChild(row);
                });

                // Update row numbers if NO column exists
                if (noColIndex !== -1) {
                    currentRows.forEach((row, idx) => {
                        if (row.children.length > noColIndex) {
                            row.children[noColIndex].textContent = (idx + 1);
                        }
                    });
                }
            });
        });
    });
});
