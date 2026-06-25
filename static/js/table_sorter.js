document.addEventListener("DOMContentLoaded", function() {
    // Inject CSS for table sorting and length select indicators
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
        .table-length-select {
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #cbd5e1;
            outline: none;
            background: white;
            cursor: pointer;
            font-size: 14px;
            color: #475569;
            transition: border-color 0.2s;
        }
        .table-length-select:focus, .table-length-select:hover {
            border-color: #0b57c6;
        }
        .page-btn {
            background: white;
            border: 1px solid #cbd5e1;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s;
        }
        .page-btn:hover:not(:disabled) {
            border-color: #0b57c6;
            color: #0b57c6;
            background-color: #F8FAFC;
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

        // Find "No" column index
        let noColIndex = -1;
        headers.forEach((header, index) => {
            const text = header.textContent.trim().toUpperCase();
            if (text === "NO" || text === "NO." || text === "#") {
                noColIndex = index;
            }
        });
        if (noColIndex === -1 && headers.length > 0) {
            const firstHeaderText = headers[0].textContent.trim();
            if (firstHeaderText === "" || firstHeaderText.length <= 3) {
                noColIndex = 0;
            }
        }

        // Find or create pagination container locally to this table/wrapper
        let paginationContainer = null;
        let sibling = table.nextElementSibling;
        if (sibling && (sibling.classList.contains('pagination-container') || sibling.classList.contains('pagination-row'))) {
            paginationContainer = sibling;
        }
        if (!paginationContainer && table.parentElement) {
            let parentSibling = table.parentElement.nextElementSibling;
            if (parentSibling && (parentSibling.classList.contains('pagination-container') || parentSibling.classList.contains('pagination-row'))) {
                paginationContainer = parentSibling;
            }
        }

        if (paginationContainer) {
            // Clean up any existing length wrappers or selectors inside the matched container
            const existing = paginationContainer.querySelectorAll('.table-length-wrapper, .per-page-selector');
            existing.forEach(el => el.remove());
            
            // Standardize container contents for client-side pagination
            paginationContainer.innerHTML = `
                <span class="pagination-text" style="font-size: 14px; color: #64748b;"></span>
                <div class="pagination-controls" style="display: flex; gap: 6px; align-items: center;"></div>
            `;
        } else {
            paginationContainer = document.createElement('div');
            paginationContainer.className = 'pagination-container';
            paginationContainer.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; border-top: 1px solid #f1f5f9;';
            paginationContainer.innerHTML = `
                <span class="pagination-text" style="font-size: 14px; color: #64748b;"></span>
                <div class="pagination-controls" style="display: flex; gap: 6px; align-items: center;"></div>
            `;
            const insertTarget = table.closest('.table-container') || table.parentElement || table;
            insertTarget.parentNode.insertBefore(paginationContainer, insertTarget.nextSibling);
        }

        // Inject page size selector
        const selectWrapper = document.createElement('div');
        selectWrapper.className = 'table-length-wrapper';
        selectWrapper.style.cssText = 'display: flex; align-items: center; gap: 8px; font-size: 14px; color: #475569; font-family: "Inter", sans-serif;';
        selectWrapper.innerHTML = `
            <span>Tampilkan</span>
            <select class="table-length-select">
                <option value="10">10</option>
                <option value="15">15</option>
                <option value="25">25</option>
            </select>
            <span>data</span>
        `;
        paginationContainer.insertBefore(selectWrapper, paginationContainer.firstChild);

        // State variables
        let currentPage = 1;
        let itemsPerPage = 10;
        let currentRows = [...originalRows];

        function updateTable() {
            const totalItems = currentRows.length;
            const totalPages = Math.ceil(totalItems / itemsPerPage);
            if (currentPage > totalPages) currentPage = Math.max(1, totalPages);

            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;

            // Clear tbody and append only the visible rows
            tbody.innerHTML = '';
            const visibleRows = currentRows.slice(start, end);

            visibleRows.forEach(row => {
                tbody.appendChild(row);
            });

            // Rewrite the row numbers (No column)
            currentRows.forEach((row, idx) => {
                if (noColIndex !== -1 && row.children.length > noColIndex) {
                    row.children[noColIndex].textContent = (idx + 1);
                }
            });

            // Update pagination text
            const textSpan = paginationContainer.querySelector('.pagination-text');
            if (textSpan) {
                const startText = totalItems === 0 ? 0 : start + 1;
                const endText = Math.min(end, totalItems);
                textSpan.textContent = `Menampilkan ${startText} - ${endText} dari ${totalItems} data`;
            }

            // Update pagination controls
            const controlsDiv = paginationContainer.querySelector('.pagination-controls');
            if (controlsDiv) {
                controlsDiv.innerHTML = '';

                // Previous button
                const prevBtn = document.createElement('button');
                prevBtn.className = 'page-btn';
                prevBtn.style.cssText = 'text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 6px; font-size: 12px;';
                prevBtn.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
                if (currentPage === 1) {
                    prevBtn.style.opacity = '0.5';
                    prevBtn.style.cursor = 'not-allowed';
                    prevBtn.disabled = true;
                } else {
                    prevBtn.addEventListener('click', () => {
                        currentPage--;
                        updateTable();
                    });
                }
                controlsDiv.appendChild(prevBtn);

                // Page buttons
                const maxPageButtons = 5;
                let startPage = Math.max(1, currentPage - Math.floor(maxPageButtons / 2));
                let endPage = Math.min(totalPages, startPage + maxPageButtons - 1);
                if (endPage - startPage + 1 < maxPageButtons) {
                    startPage = Math.max(1, endPage - maxPageButtons + 1);
                }

                for (let i = startPage; i <= endPage; i++) {
                    if (i === currentPage) {
                        const activeSpan = document.createElement('span');
                        activeSpan.className = 'page-btn active';
                        activeSpan.style.cssText = 'display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 6px; background: #0b57c6; color: white; font-weight: bold; font-size: 12px;';
                        activeSpan.textContent = i;
                        controlsDiv.appendChild(activeSpan);
                    } else {
                        const pageBtn = document.createElement('button');
                        pageBtn.className = 'page-btn';
                        pageBtn.style.cssText = 'text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 6px; font-size: 12px;';
                        pageBtn.textContent = i;
                        pageBtn.addEventListener('click', () => {
                            currentPage = i;
                            updateTable();
                        });
                        controlsDiv.appendChild(pageBtn);
                    }
                }

                // Next button
                const nextBtn = document.createElement('button');
                nextBtn.className = 'page-btn';
                nextBtn.style.cssText = 'text-decoration: none; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 6px; font-size: 12px;';
                nextBtn.innerHTML = '<i class="fa-solid fa-chevron-right"></i>';
                if (currentPage === totalPages || totalPages === 0) {
                    nextBtn.style.opacity = '0.5';
                    nextBtn.style.cursor = 'not-allowed';
                    nextBtn.disabled = true;
                } else {
                    nextBtn.addEventListener('click', () => {
                        currentPage++;
                        updateTable();
                    });
                }
                controlsDiv.appendChild(nextBtn);
            }
        }

        const lengthSelect = selectWrapper.querySelector('.table-length-select');
        lengthSelect.addEventListener('change', (e) => {
            itemsPerPage = parseInt(e.target.value, 10);
            currentPage = 1;
            updateTable();
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
                // Reset arrow indicators on other columns of this table
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

                    // Parse text/number value intelligently
                    const cleanValue = (val) => {
                        // Strip currency markers, spaces, size units
                        let cleaned = val.replace(/Rp\.?\s*/gi, '')
                                         .replace(/\.?\d+k/gi, '')
                                         .replace(/gb|tb|kg|inch|"/gi, '')
                                         .replace(/\./g, '')
                                         .replace(/,/g, '.')
                                         .trim();

                        if (!isNaN(cleaned) && cleaned !== "") {
                            return parseFloat(cleaned);
                        }

                        // Parse date if matched
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

                // Toggle sort class on click
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
                currentPage = 1;
                updateTable();
            });
        });

        // Initialize table pagination and display
        updateTable();
    });
});
