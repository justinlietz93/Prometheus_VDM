# Rules for MathJax

**Generated on:** October 3, 2025 at 1:06 PM CDT

---


**Syntax & Delimiters**

*   **TeX/LaTeX Input Configuration:**
    *   To process TeX/LaTeX, include `"input/TeX"` in the `jax` array and `"tex2jax.js"` in the `extensions` array.
    *   If you want to use single dollar signs (`$...$`) for inline math, you must explicitly enable them in your `tex2jax` configuration (e.g., `inlineMath: [['$','$'], ["\\(","\\)"]]`).
    *   When dollar signs are enabled as delimiters, you must escape a literal dollar sign using `\$`.
    *   When `processEscapes` is `false`, `\$` will not be altered.
    *   TeX input processor only implements math-mode macros, not text-mode macros (`\emph`, `\begin{enumerate}`). Use HTML for text formatting.
*   **MathML Input Configuration:**
    *   To process MathML, include `"input/MathML"` in the `jax` array and `"mml2jax.js"` in the `extensions` array.
    *   Mark displayed MathML using `<math display="block">`.
    *   Mark inline MathML using `<math display="inline">` or plain `<math>`.
*   **Preprocessor Delimiter Constraints:**
    *   Math delimiters (for `tex2jax`) cannot look like HTML tags (i.e., cannot include the less-than sign, `<`). They must consist only of text, not tags.
*   **JavaScript String Escaping:**
    *   In JavaScript strings used for configuration (e.g., `preJax`, `postJax`, `TeX.Macros` values), backslashes must be doubled (`\\`) to prevent them from acting as JavaScript escape characters.
    *   For regular expression patterns within JavaScript strings, a literal backslash `\` requires `\\\\`. A literal `\[` requires `\\[`. A literal `\\` requires `\\\\\\`.
*   **TeX Macro Definitions (`TeX.Macros`):**
    *   When defining TeX macros in `Macros` configuration, backslashes in the replacement text must be doubled (`\\`) to prevent JavaScript escaping.
    *   An array value `[value, n]` specifies replacement text and `n` parameters for the macro.
*   **Unicode Macro (`\unicode{}`):**
    *   To specify a TeX class other than ORD for `\unicode{...}` results, use `\mathbin{...}`, `\mathrel{...}`, etc.

**HTML & Page Integration**

*   **HTML Special Characters in Math:**
    *   Avoid using HTML tags within math delimiters (except `<BR>`).
    *   Avoid using `<` (less-than), `>` (greater-than), and `&` (ampersand) directly within math delimiters to prevent browser misinterpretation as HTML tags.
    *   Instead, put spaces around these symbols (e.g., `$x < y$`).
    *   Alternatively, use HTML entities `&lt;`, `&gt;`, and `&amp;` (e.g., `$x &lt; y$`).
*   **MathML in HTML:**
    *   Do not use named MathML entities (e.g., `&ApplyFunction;`). Use numeric entities (e.g., `&#x221A;`) or Unicode characters directly.
    *   In HTML documents (not XHTML), do not use self-closing tags for MathML elements with no content (e.g., use `<mspace width="thinmathspace"></mspace>` instead of `<mspace width="thinmathspace />`).
    *   Unless using XHTML, do not include a namespace prefix for `<math>` tags (e.g., do not use `<m:math>` unless `m` namespace is tied to the MathML DTD).
*   **Internet Explorer Script Tag Bug (Space Removal):**
    *   To avoid IE removing spaces around inline math `<script>` tags, use one of these solutions:
        *   Place a non-empty `<span>` element with class `MathJax_Preview` immediately before the MathJax `<script>` tag.
        *   Configure `preJax` and `postJax` in the Core Configuration Options to include guard characters. If both `preJax` and `postJax` are defined, both must be present to be removed.
*   **IE8 Standards Mode (`HTML-CSS` output):**
    *   To improve performance in IE8 when using HTML-CSS output, include `<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7">` at the very beginning of your `<head>` section, before any stylesheets or other content.
*   **CSS Style Objects:**
    *   When defining CSS styles in JavaScript objects, keys (CSS selectors or properties) containing dashes must be enclosed in quotation marks (e.g., `"background-color"`).
    *   Values in CSS style objects must be enclosed in quotation marks (e.g., `color: "red"`).
    *   Selectors in a `styles` object must be unique. If using the same selector multiple times, add comments (e.g., `".MathJax .merror /* 1 */"`) to make them unique.
*   **IE Dynamically Created Stylesheets:**
    *   Internet Explorer has a limit of 32 dynamically created stylesheets; combine styles into larger groups to avoid exceeding this limit.
    *   When changing the position of the MathJax message box for IE, you must set the side for both `#MathJax_Message` and `#MathJax_MSIE_Frame` (e.g., `styles: {"#MathJax_Message": {left: "", right: 0}, "#MathJax_MSIE_Frame": {left: "", right: 0}}`).

**Compatibility & Limitations**

*   **MathML Support Limitations:**
    *   MathJax has no support for elementary math tags: `mstack`, `mlongdiv`, `msgroup`, `msrow`, `mscarries`, `mscarry`.
    *   Line breaking is limited to direct children of `mrow` or implied `mrow` elements.
    *   No support for alignment groups in tables.
    *   No support for right-to-left rendering.
*   **TeX/LaTeX Limitations:**
    *   The TeX input processor only supports math-mode macros, not text-mode macros or environments. You must use HTML for non-mathematical text formatting.
*   **`MathJax.Ajax.Require()` File Paths:**
    *   The file path for `MathJax.Ajax.Require()` must be relative to the MathJax home directory.
    *   File paths for `MathJax.Ajax.Require()` cannot contain `../` components.

**API Usage & Asynchronous Operations**

*   **Asynchronous Operations & Synchronization:**
    *   Any MathJax operation that may cause a file to be loaded (e.g., `MathJax.Hub.Typeset()`, `MathJax.Hub.Process()`, `MathJax.Hub.Update()`) operates asynchronously.
    *   You must synchronize code that depends on the completion of MathJax's asynchronous actions using callbacks and the MathJax queue.
    *   It is always best and safest to perform typesetting operations and other actions that could load files through the MathJax queue.
*   **`MathJax.Hub.Queue()` Usage:**
    *   To place an action in the MathJax queue, use `MathJax.Hub.Queue(callback, ...)`
    *   Do not assume mathematics is visible immediately after calling `MathJax.Hub.Queue()` for typesetting; queue subsequent dependent actions as well.
    *   The items pushed onto the queue must be Callback objects (or callback specifications) that perform actions when called, not the results of calling functions.
*   **`MathJax.Hub.Typeset()` Direct Call:**
    *   Do not call `MathJax.Hub.Typeset()` directly; always queue it (`MathJax.Hub.Queue(["Typeset", MathJax.Hub]);`).
*   **Callback Specifications:**
    *   When using an object's method as a callback, use the array form `["method", object, arg1, arg2, ...]` to preserve the `this` context.
    *   A callback specified as a string (`"string"`) will be executed via `eval()` in the global context, affecting the global namespace.
*   **`MathJax.ElementJax` Operations:**
    *   When modifying individual math elements, queue the element's methods (e.g., `Text()`, `Reprocess()`) using `MathJax.Hub.Queue()` (e.g., `MathJax.Hub.Queue([ "Text", mathElementJax, "x+1"])`).
    *   When obtaining an `element jax` after MathJax's initial processing, queue the lookup: `MathJax.Hub.Queue(function() { studentDisplay = MathJax.Hub.getAllJax("MathDiv")[0]; });`
*   **`MathJax.Ajax.Require()` File Type:**
    *   The `file` argument to `MathJax.Ajax.Require()` must be a JavaScript file (`.js`) or a CSS stylesheet (`.css`).
    *   Alternatively, the `file` argument can be an object with a `js` or `css` key specifying the file.
*   **`MathJax.Callback.Signal`:**
    *   New posts to a signal are queued if a listener is in the middle of an asynchronous operation triggered by a previous post.
    *   To know when a `Post()` operation is complete, use its `callback` parameter.
    *   To prevent new listeners from receiving past messages, clear the signal history using `Signal.Clear()`.
*   **Static Properties/Methods (MathJax OOP Model):**
    *   Static values defined on an object class are not inherited by its subclasses.

## Key Highlights

* All MathJax operations that may load files (e.g., `Typeset()`, `Process()`, `Update()`) are asynchronous; dependent code must be synchronized using callbacks and the MathJax queue.
* Always queue MathJax API calls, such as `MathJax.Hub.Typeset()`, using `MathJax.Hub.Queue(["Typeset", MathJax.Hub]);` instead of calling them directly.
* Explicitly enable single dollar signs (`$...$`) for inline math in your `tex2jax` configuration and escape literal dollar signs using `\$`. Remember that the TeX input processor only supports math-mode macros; use HTML for text formatting.
* In JavaScript strings used for configuration (e.g., `preJax`, `postJax`, `TeX.Macros`), backslashes must be doubled (`\\`) to prevent them from acting as JavaScript escape characters.
* Avoid using HTML tags (except `<BR>`) and special characters (`<`, `>`, `&`) directly within math delimiters; instead, put spaces around them or use their respective HTML entities (`&lt;`, `&gt;`, `&amp;`).
* In HTML documents, do not use named MathML entities (e.g., `&ApplyFunction;`); use numeric entities (e.g., `&#x221A;`) or Unicode characters directly.
* For improved performance in IE8 when using HTML-CSS output, include `<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7">` at the very beginning of your `<head>` section.

## Example ideas

* Establish and enforce the use of `MathJax.Hub.Queue()` for all asynchronous MathJax operations (e.g., typesetting, updates, dynamic content processing) to ensure proper synchronization and prevent race conditions.
* Conduct a thorough review of server configurations to ensure correct MathJax directory permissions and verify the implementation of `Access-Control-Allow-Origin` headers for fonts, especially when serving MathJax from a different server.
* Standardize the MathJax configuration approach (e.g., `config/MathJax.js` vs. inline `MathJax.Hub.Config()`) and ensure adherence to best practices, including avoiding trailing commas in JavaScript objects for IE compatibility.
* Develop and implement guidelines for content authors and developers regarding MathJax input syntax, focusing on correct escaping of `$` (single dollar signs), backslashes in JavaScript strings, and handling of HTML special characters/tags within math delimiters.
* Create a comprehensive browser compatibility testing plan, with a specific focus on Internet Explorer, to validate the effectiveness of implemented workarounds for issues like script tag spacing, performance (`X-UA-Compatible`), and dynamic stylesheet limits.
