"""
ADEK HARIANTO QR/Barcode Scanner Android App
============================================

Aplikasi Kivy yang membungkus HTML5 WebView untuk pemindaian QR/barcode
dengan pencocokan data Excel dan export hasil.

Alur:
1. Kivy App membuat WebView Android native
2. HTML di assets/index.html dijalankan di WebView
3. Java bridge (WebViewHelper.java) menangani:
   - Izin kamera untuk getUserMedia
   - Simpan file .xlsx ke folder Download
4. Semua logika UI/scanning ada di JavaScript di index.html
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

# Set window size untuk development/preview
Window.size = (412, 732)  # Mobile size

# Import Android/Java classes
try:
    from jnius import autoclass, cast
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebChromeClient = autoclass('android.webkit.WebChromeClient')
    Uri = autoclass('android.net.Uri')
    LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
    
    try:
        WebViewHelper = autoclass('org.adekharianto.qrscan.WebViewHelper')
        HAS_WEBVIEW_HELPER = True
    except:
        HAS_WEBVIEW_HELPER = False
        WebViewHelper = None
    
    HAS_ANDROID = True
except ImportError:
    HAS_ANDROID = False
    WebViewHelper = None


class AdekHarianto(App):
    """
    Aplikasi Kivy utama yang mengelola lifecycle dan WebView.
    
    Tanggung jawab:
    - Setup window dan permissions
    - Inisialisasi WebView dengan HTML
    - Hubungkan WebView ke Java bridge (kamera + file save)
    """

    title = "ADEK HARIANTO"
    
    def build(self):
        """Build dan return widget utama (WebView atau label dev mode)."""
        
        # Container box
        layout = BoxLayout(orientation='vertical')
        
        if HAS_ANDROID:
            try:
                self._setup_android_webview(layout)
                return layout
            except Exception as e:
                layout.add_widget(Label(
                    text=f'Error setting up WebView:\n{str(e)}\n\n'
                         'Check Logcat untuk detail error.',
                    size_hint_x=1, size_hint_y=1
                ))
                return layout
        else:
            # Preview/dev mode (tanpa WebView real)
            layout.add_widget(Label(
                text='ADEK HARIANTO\n\n[Development Mode]\n\n'
                     'Aplikasi hanya berjalan di Android.\n'
                     'Untuk menjalankan:\n\n'
                     'buildozer android debug\n'
                     'atau gunakan GitHub Actions',
                size_hint_x=1, size_hint_y=1
            ))
            return layout
    
    def _setup_android_webview(self, layout):
        """Setup WebView di Android dengan izin kamera dan file bridge."""
        
        if not HAS_ANDROID:
            return
        
        # Dapatkan activity
        activity = PythonActivity.mActivity
        
        # Buat WebView
        webview = WebView(activity)
        
        # Setup WebChromeClient dengan izin kamera
        if HAS_WEBVIEW_HELPER and WebViewHelper:
            try:
                chrome_client = WebViewHelper.createChromeClient(activity)
                webview.setWebChromeClient(chrome_client)
                
                # Bind Android Bridge untuk JavaScript
                bridge = WebViewHelper.createBridge(activity)
                webview.addJavascriptInterface(bridge, "AndroidBridge")
            except Exception as e:
                print(f"Warning: Tidak bisa setup WebViewHelper: {e}")
        
        # Setup WebViewClient (handle URL loading)
        webview.setWebViewClient(WebViewClient())
        
        # Enable JavaScript dan storage
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDisplayZoomControls(False)
        settings.setBuiltInZoomControls(True)
        settings.setUseWideViewPort(True)
        settings.setLoadWithOverviewMode(True)
        
        # Set layout params
        lp = LayoutParams(
            LayoutParams.MATCH_PARENT,
            LayoutParams.MATCH_PARENT
        )
        webview.setLayoutParams(lp)
        
        # Load HTML lokal dari assets
        # Asset path di APK: file:///android_asset/assets/index.html
        webview.loadUrl("file:///android_asset/assets/index.html")
        
        # Add ke layout
        layout.add_widget(webview)


if __name__ == '__main__':
    # Jalankan aplikasi
    AdekHarianto().run()
