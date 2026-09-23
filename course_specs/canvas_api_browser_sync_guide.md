# Canvas Browser Console & Session API Sync Guide

## Overview
When an educational institution locks down the generation of personal API tokens under *Account $\rightarrow$ Settings*, instructors can still interact with Canvas's internal REST API directly by leveraging their active, authenticated browser session in Chrome or Microsoft Edge.

This technique uses the browser's existing session cookies and CSRF token (`_csrf_token`) to send programmatic `PUT`, `POST`, and `GET` requests to Canvas without requiring IT administrator approval.

---

## How It Works Under the Hood
Canvas is a single-page / AJAX-driven application. When you click **Save** on a page or edit an assignment in the Canvas web interface:
1. Your browser makes a standard `fetch()` or `XMLHttpRequest` to Canvas's internal REST API endpoint (e.g. `/api/v1/courses/:course_id/pages/:page_url`).
2. Your browser automatically attaches your authenticated session cookie.
3. Canvas requires a CSRF token to prevent cross-site request forgery, which is stored in a cookie named `_csrf_token`.
4. By reading `_csrf_token` from `document.cookie` and passing it in the `X-CSRF-Token` header, you can perform any action your instructor account is authorized to do.

---

## Step-by-Step Instructions

### Step 1: Open Your Canvas Course in Chrome or Edge
1. Navigate to your course home page in Canvas (e.g., `https://lccc-wy.instructure.com/courses/18381`).
2. Note your **Course ID** from the URL (in the example above, `18381`).

### Step 2: Open Developer Tools Console
1. Press `F12` (or right-click anywhere on the page and select **Inspect**).
2. Click on the **Console** tab.

### Step 3: Run the Synchronous Update Snippet

#### A. Updating an Existing Page
Copy and paste this snippet into the Console, replacing `COURSE_ID`, `PAGE_URL`, and `PAGE_HTML` with your desired values:

```javascript
(async function updateCanvasPage(courseId, pageUrl, newTitle, newHtml) {
    const csrfToken = decodeURIComponent(document.cookie.match(/_csrf_token=([^;]+)/)[1]);
    
    console.log(`⏳ Updating page: ${pageUrl}...`);
    
    const response = await fetch(`/api/v1/courses/${courseId}/pages/${pageUrl}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken
        },
        body: JSON.stringify({
            wiki_page: {
                title: newTitle,
                body: newHtml
            }
        })
    });
    
    if (response.ok) {
        console.log(`✅ Successfully updated ${pageUrl}! Refreshing page in 2s...`);
        setTimeout(() => location.reload(), 2000);
    } else {
        const error = await response.json();
        console.error('❌ Update failed:', error);
    }
})(
    '18381',                   // YOUR_COURSE_ID
    'unit-1-overview',         // PAGE_URL_SLUG
    'Unit 1: Overview',        // PAGE_TITLE
    '<div>Your HTML here</div>'// NEW_HTML_CONTENT
);
```

#### B. Exporting a Page's HTML (Backup / Scraping)
If you want to extract the exact raw HTML of any Canvas page for archival:

```javascript
(async function getCanvasPageHtml(courseId, pageUrl) {
    const response = await fetch(`/api/v1/courses/${courseId}/pages/${pageUrl}`);
    const data = await response.json();
    console.log("=== PAGE TITLE ===", data.title);
    console.log("=== RAW HTML ===", data.body);
    
    // Copy directly to clipboard!
    copy(data.body);
    console.log("✅ Raw HTML copied directly to your clipboard!");
})('18381', 'unit-1-overview');
```

---

## Creating a 1-Click Bookmarklet
To make this a 1-click tool without opening DevTools every time:
1. Open your browser bookmarks bar (`Ctrl+Shift+O`).
2. Add a new bookmark:
   * **Name:** `Canvas Page Sync`
   * **URL:** Paste the JavaScript code prefixed with `javascript:(function(){ ... })();`.
3. Whenever you are viewing a page in Canvas, clicking the bookmarklet will trigger the sync prompt!
