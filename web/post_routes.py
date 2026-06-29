<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fast Finder – Admin Panel</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
/* ── EXACT web_assets.py CSS VARIABLES ── */
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0a0a0c;--bg2:#111116;--bg3:#1d1d26;--bg4:#2a2a38;
  --accent:#e50914;--accent-hover:#b30710;
  --text:#ffffff;--muted:#a0a0b0;--border:#262636;--card:#14141f;
}
.light{
  --bg:#f4f5f7;--bg2:#ffffff;--bg3:#eef0f4;--bg4:#dbdee6;
  --text:#0a0a0c;--muted:#62627a;--border:#d2d5df;--card:#ffffff;
}

body{
  font-family:'DM Sans',sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
  transition:background .2s,color .2s;
}

/* ── TOPBAR ── */
.topbar{
  background:var(--bg2);padding:0 4%;
  display:flex;align-items:center;height:68px;
  position:sticky;top:0;z-index:100;gap:15px;
  box-shadow:0 4px 20px rgba(0,0,0,0.4);
  border-bottom:1px solid var(--border);
}
.ham-btn{background:none;border:none;cursor:pointer;color:var(--text);display:flex;flex-direction:column;gap:5px;padding:6px;}
.ham-line{width:22px;height:2px;background:currentColor;transition:.2s;display:block;}
.logo{font-size:18px;font-weight:900;letter-spacing:1px;color:var(--accent);display:flex;align-items:center;gap:8px;text-decoration:none;flex:1;}
.nf-icon{background:var(--accent);color:#fff;padding:2px 7px;border-radius:3px;font-size:18px;line-height:1;}
.theme-btn{margin-left:auto;background:none;border:1px solid var(--border);border-radius:4px;padding:6px 14px;font-size:12px;font-weight:700;color:var(--text);cursor:pointer;font-style:italic;transition:.15s;}
.theme-btn:hover{background:var(--bg3);}

/* ── SIDEBAR ── */
.sidebar-overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:150;opacity:0;pointer-events:none;transition:.2s;}
.sidebar-overlay.open{opacity:1;pointer-events:all;}
.sidebar{position:fixed;top:0;left:0;height:100%;width:260px;background:var(--bg2);border-right:1px solid var(--border);z-index:160;display:flex;flex-direction:column;transform:translateX(-100%);transition:.3s;}
.sidebar.open{transform:translateX(0);}
.sb-header{padding:20px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;}
.sb-logo{font-size:14px;font-weight:900;color:var(--accent);display:flex;align-items:center;gap:8px;}
.sb-close{background:none;border:none;color:var(--muted);font-size:22px;cursor:pointer;}
.sb-nav{padding:15px 10px;flex:1;}
.sb-section{font-size:11px;font-weight:700;color:var(--muted);padding:8px 12px;letter-spacing:1px;text-transform:uppercase;}
.sb-link{display:flex;align-items:center;gap:10px;padding:12px 15px;border-radius:4px;text-decoration:none;color:var(--muted);font-size:15px;font-weight:500;margin-bottom:4px;transition:.15s;}
.sb-link:hover{background:var(--bg3);color:var(--text);}
.sb-link.active{background:var(--accent);color:#fff;}
.sb-footer{padding:15px 10px;border-top:1px solid var(--border);}
.sb-logout{display:block;padding:12px;border-radius:4px;text-align:center;text-decoration:none;color:var(--text);font-weight:700;border:1px solid var(--border);transition:.15s;}
.sb-logout:hover{background:var(--bg3);}

/* ── PAGE LAYOUT ── */
.page-wrap{padding:24px 4% 60px;max-width:880px;margin:0 auto;}
.page-header{display:flex;align-items:center;gap:14px;margin-bottom:24px;}
.back-link{background:var(--bg3);border:1px solid var(--border);color:var(--muted);padding:9px 16px;border-radius:6px;font-size:13px;font-weight:700;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:4px;transition:.15s;}
.back-link:hover{background:var(--bg4);color:var(--text);}
.page-title{font-size:26px;font-weight:900;color:var(--text);}

/* ── TAB SWITCHER ── */
.tab-switcher{display:flex;gap:8px;margin-bottom:22px;}
.sw-tab{flex:1;background:var(--card);border:1px solid var(--border);padding:12px;border-radius:8px;font-size:12px;font-weight:800;text-align:center;cursor:pointer;color:var(--muted);letter-spacing:.5px;text-transform:uppercase;transition:.2s;}
.sw-tab:hover:not(.active){background:var(--bg3);color:var(--text);}
.sw-tab.active{background:var(--accent);border-color:var(--accent);color:#fff;}

/* ── STEP CARDS ── */
.step-box{background:var(--card);border:1px solid var(--border);padding:24px;border-radius:12px;margin-bottom:18px;box-shadow:0 8px 25px rgba(0,0,0,.2);}
.step-box.accent-box{border-color:var(--accent);}
.step-header{display:flex;align-items:center;gap:12px;margin-bottom:20px;padding-bottom:14px;border-bottom:1px solid var(--border);}
.step-num{width:30px;height:30px;border-radius:50%;background:var(--bg4);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;color:var(--text);flex-shrink:0;}
.step-num.red{background:var(--accent);color:#fff;}
.step-title{font-size:13px;font-weight:900;color:var(--text);letter-spacing:1px;text-transform:uppercase;}
.step-title.red{color:var(--accent);}

/* ── FORM ELEMENTS (exact web_assets .em-input) ── */
.scard-label{font-size:12px;font-weight:700;color:var(--muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:1px;display:block;}
.em-input{width:100%;background:var(--bg);border:1px solid var(--border);padding:12px 14px;color:var(--text);margin-bottom:15px;border-radius:6px;outline:none;font-family:'DM Sans',sans-serif;font-size:14px;transition:border-color .2s;}
.em-input:focus{border-color:var(--accent);}
textarea.em-input{min-height:110px;resize:vertical;line-height:1.6;}
.em-input::placeholder{color:var(--muted);}

/* ── DIVIDER ── */
.divider-or{text-align:center;color:var(--muted);font-size:11px;font-weight:800;letter-spacing:1px;margin:12px 0;position:relative;}
.divider-or::before,.divider-or::after{content:'';position:absolute;top:50%;height:1px;background:var(--border);}
.divider-or::before{left:0;width:calc(50% - 70px);}
.divider-or::after{right:0;width:calc(50% - 70px);}

/* ── UPLOAD BUTTON ── */
.em-upload-btn{display:flex;align-items:center;gap:12px;background:var(--bg4);border:1px dashed var(--border);padding:14px 16px;border-radius:8px;cursor:pointer;font-weight:700;font-size:13px;color:var(--text);transition:.2s;width:100%;margin-top:10px;}
.em-upload-btn:hover{background:var(--bg3);border-color:var(--muted);}
.upload-icon-box{width:36px;height:36px;background:var(--bg3);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;}
.upload-label-main{font-size:14px;font-weight:700;}
.upload-label-sub{font-size:11px;color:var(--muted);margin-top:2px;font-weight:400;}

/* ── COVER PREVIEW GRID ── */
.cover-preview-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;}
.cover-thumb{position:relative;background:var(--bg3);border-radius:8px;overflow:hidden;aspect-ratio:1;border:1px solid var(--border);}
.cover-thumb-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.cover-thumb-label{position:absolute;bottom:0;left:0;right:0;text-align:center;font-size:12px;font-weight:800;color:#fff;background:rgba(0,0,0,.65);padding:7px;}

/* ── VIDEO SEARCH ── */
.search-row{display:flex;gap:8px;margin-bottom:12px;}
.search-row .em-input{margin-bottom:0;flex:1;}
.search-btn{background:var(--accent);color:#fff;border:none;padding:0 22px;border-radius:6px;font-size:14px;font-weight:800;cursor:pointer;white-space:nowrap;transition:.15s;font-family:'DM Sans',sans-serif;}
.search-btn:hover{background:var(--accent-hover);}
.search-btn:active{transform:scale(.96);}

/* ── SEARCH RESULTS DROPDOWN ── */
.search-results{background:var(--bg2);border:1px solid var(--border);border-radius:6px;max-height:220px;overflow-y:auto;display:none;margin-bottom:14px;box-shadow:0 4px 15px rgba(0,0,0,.5);}
.search-result-item{padding:12px 15px;border-bottom:1px solid var(--border);cursor:pointer;transition:.15s;}
.search-result-item:last-child{border-bottom:none;}
.search-result-item:hover{background:var(--bg3);}
.sri-name{font-weight:700;font-size:13px;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.sri-size{font-size:11px;color:var(--muted);margin-top:3px;}
.sri-size span{background:var(--bg4);padding:2px 6px;border-radius:4px;font-weight:600;}

/* ── SELECTED VIDEOS ── */
.selected-vids-wrap{display:flex;flex-direction:column;gap:10px;min-height:60px;}
.selected-vids-empty{min-height:60px;display:flex;align-items:center;justify-content:center;background:var(--bg);border:1px dashed var(--border);border-radius:8px;padding:16px;}
.no-vids-msg{color:var(--muted);font-size:13px;font-weight:600;text-align:center;}
.vid-entry{background:var(--card);border:1px solid var(--accent);padding:15px;border-radius:8px;display:flex;gap:14px;align-items:flex-start;}
.vid-entry-info{flex:1;min-width:0;}
.vid-entry-fname{font-size:11px;color:var(--muted);margin-bottom:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.vid-remove-btn{background:rgba(160,8,8,.78);color:#fff;border:none;padding:10px 14px;border-radius:6px;cursor:pointer;font-weight:700;flex-shrink:0;font-size:14px;transition:.15s;}
.vid-remove-btn:hover{background:var(--accent);}

/* ── SUBMIT BUTTON ── */
.submit-btn{width:100%;background:var(--accent);color:#fff;border:none;padding:17px;border-radius:8px;font-weight:700;font-size:16px;cursor:pointer;box-shadow:0 8px 25px rgba(229,9,20,.4);transition:.2s;font-family:'DM Sans',sans-serif;font-style:italic;letter-spacing:.5px;margin-top:4px;}
.submit-btn:hover{background:var(--accent-hover);transform:translateY(-1px);box-shadow:0 12px 30px rgba(229,9,20,.5);}
.submit-btn:active{transform:scale(.98);}

/* ── TOAST (exact web_assets) ── */
.toast{position:fixed;bottom:20px;right:20px;background:var(--accent);color:#fff;padding:12px 20px;border-radius:4px;font-weight:700;z-index:300;transform:translateX(150%);transition:.3s;font-size:13px;max-width:280px;}
.toast.show{transform:translateX(0);}
.toast.error{background:#000;border:1px solid var(--accent);}

/* ── SUCCESS / ERROR BOXES (form_wrapper style) ── */
.err-box{background:#e87c03;color:#fff;padding:10px 20px;border-radius:4px;margin-bottom:16px;font-size:14px;font-weight:600;}
.success-box{background:#28a745;color:#fff;padding:10px 20px;border-radius:4px;margin-bottom:16px;font-size:14px;font-weight:600;}

/* ── RESPONSIVE ── */
@media(max-width:600px){
  .page-wrap{padding:16px 4% 60px;}
  .page-title{font-size:20px;}
  .step-box{padding:16px;}
  .cover-preview-grid{grid-template-columns:1fr 1fr;}
}

/* ── TAB VISIBILITY ── */
#tab-create, #tab-edit{display:none;}
#tab-create.show, #tab-edit.show{display:block;}
</style>
</head>
<body>

<!-- ── SIDEBAR OVERLAY ── -->
<div class="sidebar-overlay" id="sbOverlay" onclick="closeSidebar()"></div>

<!-- ── SIDEBAR ── -->
<div class="sidebar" id="sidebar">
  <div class="sb-header">
    <div class="sb-logo"><span class="nf-icon">F</span> FAST FINDER</div>
    <button class="sb-close" onclick="closeSidebar()">&#10005;</button>
  </div>
  <nav class="sb-nav">
    <div class="sb-section">Menu</div>
    <a href="/dashboard" class="sb-link">🏠 Home</a>
    <a href="/posts"     class="sb-link active">📝 Posts</a>
    <a href="/actors"    class="sb-link">🎭 Actors</a>
    <a href="/stats"     class="sb-link">📊 Database Stats</a>
    <a href="/profile"   class="sb-link">⚙️ Profile Settings</a>
  </nav>
  <div class="sb-footer">
    <a href="/logout" class="sb-logout">Sign Out</a>
  </div>
</div>

<!-- ── TOPBAR ── -->
<div class="topbar">
  <button class="ham-btn" id="hamBtn" onclick="openSidebar()">
    <span class="ham-line"></span>
    <span class="ham-line"></span>
    <span class="ham-line"></span>
  </button>
  <a class="logo" href="/dashboard"><span class="nf-icon">F</span> FAST FINDER</a>
  <button class="theme-btn" onclick="toggleThemeFixed()">Theme</button>
</div>

<!-- ── MAIN CONTENT ── -->
<div class="page-wrap">

  <!-- Tab Switcher -->
  <div class="tab-switcher">
    <div class="sw-tab active" onclick="switchTab('create')" id="sw-create">➕ Create New Post</div>
    <div class="sw-tab"        onclick="switchTab('edit')"   id="sw-edit">✏️ Edit Post</div>
  </div>

  <!-- ════════════════════════════════════════════
       CREATE NEW POST TAB
       ════════════════════════════════════════════ -->
  <div id="tab-create" class="show">

    <div class="page-header">
      <a href="/posts" class="back-link">← Posts</a>
      <div class="page-title">Create New Post</div>
    </div>

    <form id="createForm" action="/api/post/publish" method="post" enctype="multipart/form-data">

      <!-- STEP 1: Basic Info -->
      <div class="step-box">
        <div class="step-header">
          <div class="step-num">1</div>
          <div class="step-title">Basic Information</div>
        </div>
        <label class="scard-label">Post Title</label>
        <input class="em-input" type="text" name="title" placeholder="e.g. Panchayat S03 or Pushpa 2" required>

        <label class="scard-label">Short Description</label>
        <textarea class="em-input" name="description" placeholder="Write a short description about this post..." required></textarea>

        <label class="scard-label">Search Tags (Comma Separated)</label>
        <input class="em-input" type="text" name="tags" placeholder="e.g. Action, Web Series, 2024, Hindi" style="margin-bottom:0">
      </div>

      <!-- STEP 2: Cover Image -->
      <div class="step-box">
        <div class="step-header">
          <div class="step-num">2</div>
          <div class="step-title">Cover Image</div>
        </div>
        <label class="scard-label">Paste Image URL (ibb.co or Direct Link)</label>
        <input class="em-input" type="text" name="cover_url" id="c-cover-url" placeholder="https://i.ibb.co/..." oninput="previewCoverUrl(this.value,'c-cover-preview')">

        <div id="c-cover-preview" style="display:none;width:100%;max-width:260px;aspect-ratio:16/9;background:var(--bg3);border:1px solid var(--border);border-radius:8px;overflow:hidden;margin-bottom:14px;">
          <img id="c-cover-preview-img" src="" alt="Preview" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentElement.style.display='none'">
        </div>

        <div class="divider-or">OR UPLOAD FILE</div>
        <label class="em-upload-btn">
          <div class="upload-icon-box">🖼️</div>
          <div>
            <div class="upload-label-main">Choose Cover Image</div>
            <div class="upload-label-sub" id="c-cover-sub">No file chosen</div>
          </div>
          <input type="file" name="cover_file" accept="image/*" style="display:none" onchange="updateFileSub(this,'c-cover-sub'); previewLocalFile(this,'c-cover-preview','c-cover-preview-img')">
        </label>
      </div>

      <!-- STEP 3: Screenshots -->
      <div class="step-box">
        <div class="step-header">
          <div class="step-num">3</div>
          <div class="step-title">Screenshots</div>
        </div>
        <label class="scard-label">Paste ibb.co Links (One per Line)</label>
        <textarea class="em-input" name="screenshot_urls" placeholder="https://i.ibb.co/link1&#10;https://i.ibb.co/link2&#10;..."></textarea>

        <div class="divider-or">AND / OR UPLOAD FILES</div>
        <label class="em-upload-btn">
          <div class="upload-icon-box">📸</div>
          <div>
            <div class="upload-label-main">Choose Screenshots</div>
            <div class="upload-label-sub" id="c-ss-sub">No files chosen</div>
          </div>
          <input type="file" name="screenshot_files" accept="image/*" multiple style="display:none" onchange="updateFileSub(this,'c-ss-sub')">
        </label>
      </div>

      <!-- STEP 4: Videos/Episodes -->
      <div class="step-box accent-box">
        <div class="step-header" style="border-bottom-color:rgba(229,9,20,.3)">
          <div class="step-num red">4</div>
          <div class="step-title red">Videos / Episodes</div>
        </div>

        <div class="search-row">
          <input class="em-input" type="text" id="c-vid-search" placeholder="Search and add more files..."
            onkeydown="if(event.key==='Enter'){event.preventDefault();searchVideos('c');}">
          <button type="button" class="search-btn" onclick="searchVideos('c')">Search</button>
        </div>

        <div class="search-results" id="c-search-results"></div>

        <label class="scard-label">Selected Videos / Episodes</label>
        <div id="c-selected-vids">
          <div class="selected-vids-empty">
            <div class="no-vids-msg">No videos added yet. Search above to add files.</div>
          </div>
        </div>
      </div>

      <button type="submit" class="submit-btn" onclick="handleSubmit(event,'createForm')">🚀 Publish Post</button>
    </form>
  </div>

  <!-- ════════════════════════════════════════════
       EDIT POST TAB
       ════════════════════════════════════════════ -->
  <div id="tab-edit">

    <div class="page-header">
      <a href="#" onclick="history.back();return false;" class="back-link">← Cancel</a>
      <div class="page-title">Edit Post</div>
    </div>

    <form id="editForm" action="/api/post/update" method="post" enctype="multipart/form-data">
      <input type="hidden" name="post_id" id="edit-post-id" value="">

      <!-- STEP 1: Basic Info -->
      <div class="step-box">
        <div class="step-header">
          <div class="step-num">1</div>
          <div class="step-title">Basic Information</div>
        </div>
        <label class="scard-label">Post Title</label>
        <input class="em-input" type="text" name="title" id="edit-title" placeholder="Post title" required>

        <label class="scard-label">Short Description</label>
        <textarea class="em-input" name="description" id="edit-desc" placeholder="Short description..." required></textarea>

        <label class="scard-label">Search Tags (Comma Separated)</label>
        <input class="em-input" type="text" name="tags" id="edit-tags" placeholder="e.g. Action, Web Series, 2024" style="margin-bottom:0">
      </div>

      <!-- STEP 2: Cover Image -->
      <div class="step-box">
        <div class="step-header">
          <div class="step-num">2</div>
          <div class="step-title">Cover Image</div>
        </div>

        <!-- Existing cover previews -->
        <div class="cover-preview-grid" id="edit-cover-grid" style="display:none"></div>

        <label class="scard-label">New Image URL (Leave Blank to Keep Current)</label>
        <input class="em-input" type="text" name="cover_url" id="e-cover-url"
          placeholder="Telegram-hosted image (current)"
          oninput="previewCoverUrl(this.value,'e-cover-preview')">

        <div id="e-cover-preview" style="display:none;width:100%;max-width:260px;aspect-ratio:16/9;background:var(--bg3);border:1px solid var(--border);border-radius:8px;overflow:hidden;margin-bottom:14px;">
          <img id="e-cover-preview-img" src="" alt="Preview" style="width:100%;height:100%;object-fit:cover;" onerror="this.parentElement.style.display='none'">
        </div>

        <div class="divider-or">OR UPLOAD NEW FILE</div>
        <label class="em-upload-btn">
          <div class="upload-icon-box">🖼️</div>
          <div>
            <div class="upload-label-main">Replace Cover Image</div>
            <div class="upload-label-sub" id="e-cover-sub">No file chosen</div>
          </div>
          <input type="file" name="cover_file" accept="image/*" style="display:none"
            onchange="updateFileSub(this,'e-cover-sub'); previewLocalFile(this,'e-cover-preview','e-cover-preview-img')">
        </label>
      </div>

      <!-- STEP 3: Screenshots -->
      <div class="step-box">
        <div class="step-header">
          <div class="step-num">3</div>
          <div class="step-title">Screenshots</div>
        </div>
        <label class="scard-label">Image URLs (One per Line)</label>
        <textarea class="em-input" name="screenshot_urls" id="edit-ss-urls" placeholder="TG_ID:... or https://..."></textarea>

        <div class="divider-or">AND / OR UPLOAD NEW FILES</div>
        <label class="em-upload-btn">
          <div class="upload-icon-box">📸</div>
          <div>
            <div class="upload-label-main">Add More Screenshots</div>
            <div class="upload-label-sub" id="e-ss-sub">No files chosen</div>
          </div>
          <input type="file" name="screenshot_files" accept="image/*" multiple style="display:none"
            onchange="updateFileSub(this,'e-ss-sub')">
        </label>
      </div>

      <!-- STEP 4: Videos -->
      <div class="step-box accent-box">
        <div class="step-header" style="border-bottom-color:rgba(229,9,20,.3)">
          <div class="step-num red">4</div>
          <div class="step-title red">Videos / Episodes</div>
        </div>

        <div class="search-row">
          <input class="em-input" type="text" id="e-vid-search" placeholder="Search and add more files..."
            onkeydown="if(event.key==='Enter'){event.preventDefault();searchVideos('e');}">
          <button type="button" class="search-btn" onclick="searchVideos('e')">Search</button>
        </div>

        <div class="search-results" id="e-search-results"></div>

        <label class="scard-label">Current Videos / Episodes</label>
        <div id="e-selected-vids">
          <div class="selected-vids-empty">
            <div class="no-vids-msg">No videos added yet. Search above to add files.</div>
          </div>
        </div>
      </div>

      <button type="submit" class="submit-btn" onclick="handleSubmit(event,'editForm')">💾 Save Changes</button>
    </form>
  </div>

</div><!-- /page-wrap -->

<!-- ── TOAST ── -->
<div class="toast" id="toast"></div>

<!-- ════════════════════════════════════════════
     JAVASCRIPT — ALL FEATURES
     ════════════════════════════════════════════ -->
<script>
/* ── THEME (exact web_assets.py logic) ── */
(function(){
  if(localStorage.getItem('theme')==='light')
    document.documentElement.classList.add('light');
})();
function toggleThemeFixed(){
  var l = document.documentElement.classList.toggle('light');
  localStorage.setItem('theme', l ? 'light' : 'dark');
}

/* ── SIDEBAR ── */
function openSidebar(){
  document.getElementById('sidebar').classList.add('open');
  document.getElementById('sbOverlay').classList.add('open');
}
function closeSidebar(){
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sbOverlay').classList.remove('open');
}

/* ── TAB SWITCHER ── */
function switchTab(t) {
  document.getElementById('sw-create').classList.toggle('active', t==='create');
  document.getElementById('sw-edit').classList.toggle('active', t==='edit');
  document.getElementById('tab-create').classList.toggle('show', t==='create');
  document.getElementById('tab-edit').classList.toggle('show', t==='edit');
}

/* ── TOAST (exact web_assets.py) ── */
var _tt;
function showToast(m, type) {
  type = type || 'success';
  var x = document.getElementById('toast');
  x.textContent = m;
  x.className = 'toast ' + type + ' show';
  clearTimeout(_tt);
  _tt = setTimeout(function(){ x.classList.remove('show'); }, 3000);
}

/* ── FILE INPUT LABEL ── */
function updateFileSub(input, subId) {
  var sub = document.getElementById(subId);
  if (!sub || !input.files.length) return;
  sub.textContent = input.files.length === 1
    ? input.files[0].name
    : input.files.length + ' files chosen';
}

/* ── LOCAL FILE PREVIEW (cover image) ── */
function previewLocalFile(input, wrapId, imgId) {
  if (!input.files || !input.files[0]) return;
  var reader = new FileReader();
  reader.onload = function(e) {
    var wrap = document.getElementById(wrapId);
    var img  = document.getElementById(imgId);
    if (wrap && img) {
      img.src = e.target.result;
      wrap.style.display = 'block';
    }
  };
  reader.readAsDataURL(input.files[0]);
}

/* ── URL PREVIEW (cover image) ── */
function previewCoverUrl(url, wrapId) {
  var trimmed = url.trim();
  var wrap = document.getElementById(wrapId);
  if (!wrap) return;
  if (trimmed.startsWith('http')) {
    var imgId = wrapId + '-img';
    var img = document.getElementById(imgId);
    if (img) { img.src = trimmed; }
    wrap.style.display = 'block';
  } else {
    wrap.style.display = 'none';
  }
}

/* ── VIDEO SEARCH ──
   Calls your actual backend /api/search endpoint.
   Falls back to demo mode if fetch fails (for standalone preview).
── */
async function searchVideos(tab) {
  var inputEl    = document.getElementById(tab + '-vid-search');
  var resultsDiv = document.getElementById(tab + '-search-results');
  var q = inputEl.value.trim();
  if (!q) { showToast('Kuch type karein phir search karein', 'error'); return; }

  resultsDiv.innerHTML = '<div style="padding:14px;text-align:center;color:var(--muted);font-weight:600;">🔍 Searching...</div>';
  resultsDiv.style.display = 'block';

  try {
    var res  = await fetch('/api/search?q=' + encodeURIComponent(q) + '&mode=none');
    var data = await res.json();

    if (!data.results || data.results.length === 0) {
      resultsDiv.innerHTML = '<div style="padding:14px;text-align:center;color:var(--muted);">❌ Koi file nahi mili.</div>';
      return;
    }
    var html = '';
    data.results.forEach(function(f) {
      var safeName = f.name.replace(/'/g,"\\'").replace(/"/g,'&quot;');
      html += '<div class="search-result-item" onclick="addVideoEntry(\'' + tab + '\',\'' + f.file_id + '\',\'' + safeName + '\')">'
            + '<div class="sri-name">📁 ' + f.name + '</div>'
            + '<div class="sri-size"><span>' + (f.size || '') + '</span></div>'
            + '</div>';
    });
    resultsDiv.innerHTML = html;

  } catch(e) {
    /* ── DEMO fallback (for standalone preview without backend) ── */
    var demoFiles = [
      {file_id:'DEMO001', name: q + ' [1080p].mkv',    size:'2.1 GB'},
      {file_id:'DEMO002', name: q + ' [720p].mkv',     size:'1.2 GB'},
      {file_id:'DEMO003', name: q + ' [Episode 1].mkv',size:'450 MB'},
    ];
    var html = '';
    demoFiles.forEach(function(f){
      var safeName = f.name.replace(/'/g,"\\'");
      html += '<div class="search-result-item" onclick="addVideoEntry(\'' + tab + '\',\'' + f.file_id + '\',\'' + safeName + '\')">'
            + '<div class="sri-name">📁 ' + f.name + '</div>'
            + '<div class="sri-size"><span>' + f.size + '</span></div>'
            + '</div>';
    });
    resultsDiv.innerHTML = html;
  }
}

/* ── CLOSE SEARCH RESULTS ON OUTSIDE CLICK ── */
document.addEventListener('click', function(e) {
  ['c-search-results','e-search-results'].forEach(function(id){
    var el = document.getElementById(id);
    if (el && !el.contains(e.target) && !e.target.classList.contains('search-btn')) {
      el.style.display = 'none';
    }
  });
});

/* ── ADD VIDEO ENTRY ── */
function addVideoEntry(tab, fileId, fileName) {
  document.getElementById(tab + '-search-results').style.display = 'none';
  document.getElementById(tab + '-vid-search').value = '';

  var container = document.getElementById(tab + '-selected-vids');

  /* Remove empty state if present */
  var emptyEl = container.querySelector('.selected-vids-empty');
  if (emptyEl) emptyEl.remove();

  /* Ensure wrapper div */
  var wrap = container.querySelector('.selected-vids-wrap');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.className = 'selected-vids-wrap';
    container.appendChild(wrap);
  }

  var div = document.createElement('div');
  div.className = 'vid-entry';
  div.innerHTML =
    '<div class="vid-entry-info">'
    + '<div class="vid-entry-fname">📁 ' + fileName + '</div>'
    + '<input type="hidden" name="video_id" value="' + fileId + '">'
    + '<input type="text" name="video_heading" placeholder="Group Name (e.g. Episode 1 or Movie Links)" class="em-input" style="margin-bottom:9px;font-weight:700;" required>'
    + '<input type="text" name="video_name" placeholder="Quality (e.g. 1080p)" class="em-input" style="margin-bottom:0;font-weight:800;color:var(--accent);" required>'
    + '</div>'
    + '<button type="button" class="vid-remove-btn" onclick="removeVidEntry(this,\'' + tab + '\')">✖</button>';

  wrap.appendChild(div);
  showToast('✅ File add hua! Details bharein.');
}

/* ── REMOVE VIDEO ENTRY ── */
function removeVidEntry(btn, tab) {
  var entry = btn.closest('.vid-entry');
  if (entry) entry.remove();

  var wrap = document.getElementById(tab + '-selected-vids').querySelector('.selected-vids-wrap');
  if (wrap && wrap.children.length === 0) {
    wrap.remove();
    var container = document.getElementById(tab + '-selected-vids');
    container.innerHTML = '<div class="selected-vids-empty"><div class="no-vids-msg">No videos added yet. Search above to add files.</div></div>';
  }
  showToast('File remove hua.');
}

/* ── FORM SUBMIT ── */
function handleSubmit(e, formId) {
  /* Let the form submit normally to backend.
     Only intercept if we want client-side validation. */
  var form = document.getElementById(formId);

  /* Basic validation */
  var titleEl = form.querySelector('[name="title"]');
  var descEl  = form.querySelector('[name="description"]');
  if (titleEl && !titleEl.value.trim()) {
    e.preventDefault();
    showToast('Title likhna zaroori hai!', 'error');
    titleEl.focus();
    return;
  }
  if (descEl && !descEl.value.trim()) {
    e.preventDefault();
    showToast('Description likhna zaroori hai!', 'error');
    descEl.focus();
    return;
  }
  /* All good — form will submit to backend naturally */
  showToast('⏳ Saving...');
}

/* ── POPULATE EDIT FORM (call this from your post list page) ──
   Example usage from another page:
   window.location.href = '/admin_ui.html?mode=edit&post_id=...&title=...&desc=...&tags=...&cover=...&ss=...&videos=...'
── */
function populateEditForm(data) {
  document.getElementById('edit-post-id').value  = data.post_id  || '';
  document.getElementById('edit-title').value    = data.title    || '';
  document.getElementById('edit-desc').value     = data.desc     || '';
  document.getElementById('edit-tags').value     = data.tags     || '';
  document.getElementById('edit-ss-urls').value  = data.ss_urls  || '';
  document.getElementById('e-cover-url').value   = data.cover    || '';

  /* Show existing cover previews */
  if (data.cover_images && data.cover_images.length) {
    var grid = document.getElementById('edit-cover-grid');
    grid.innerHTML = '';
    data.cover_images.forEach(function(item) {
      var src = item.url || '';
      grid.innerHTML += '<div class="cover-thumb">'
        + '<img class="cover-thumb-img" src="' + src + '" onerror="this.style.display=\'none\'">'
        + '<div class="cover-thumb-label">' + (item.label || '') + '</div>'
        + '</div>';
    });
    grid.style.display = 'grid';
  }

  /* Pre-load existing videos */
  if (data.videos && data.videos.length) {
    var container = document.getElementById('e-selected-vids');
    container.innerHTML = '<div class="selected-vids-wrap"></div>';
    var wrap = container.querySelector('.selected-vids-wrap');
    data.videos.forEach(function(v) {
      var div = document.createElement('div');
      div.className = 'vid-entry';
      div.innerHTML =
        '<div class="vid-entry-info">'
        + '<div class="vid-entry-fname">📁 Pre-selected Media</div>'
        + '<input type="hidden" name="video_id" value="' + v.file_id + '">'
        + '<input type="text" name="video_heading" value="' + (v.heading||'') + '" placeholder="Group Name" class="em-input" style="margin-bottom:9px;font-weight:700;" required>'
        + '<input type="text" name="video_name" value="' + (v.custom_name||'') + '" placeholder="Quality (e.g. 1080p)" class="em-input" style="margin-bottom:0;font-weight:800;color:var(--accent);" required>'
        + '</div>'
        + '<button type="button" class="vid-remove-btn" onclick="removeVidEntry(this,\'e\')">✖</button>';
      wrap.appendChild(div);
    });
  }

  switchTab('edit');
}

/* ── URL PARAMS: auto-populate edit form if ?mode=edit&... ── */
(function() {
  var params = new URLSearchParams(window.location.search);
  if (params.get('mode') === 'edit') {
    populateEditForm({
      post_id: params.get('post_id') || '',
      title:   params.get('title')   || '',
      desc:    params.get('desc')    || '',
      tags:    params.get('tags')    || '',
      cover:   params.get('cover')   || '',
      ss_urls: params.get('ss')      || '',
    });
  }
})();
</script>
</body>
</html>
