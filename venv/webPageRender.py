import webview

html = """<!doctype html>

                <html lang="en">
                <head>
                    <meta charset="utf-8">

                    <title>The HTML5 Herald</title>
                    <meta name="description" content="The HTML5 Herald">
                    <meta name="author" content="SitePoint">

                     <link rel="stylesheet" href="css/styles.css?v=1.0">

                </head>

                <body>
                    <h1>This site is created in python</h1>
                    </br>
                    <img src="  """ + r"""file:///C:\Users\nekol\Documents\PycharmProjects\webSite-generator\venv\Site\python.png" alt="python" width="100" height="100">
                    </br>
                    <h2>Author: Tony Nekola</h2>
                    </br>
                </body>
                </html>"""

html1 = """
  <html>
    <body>
      <h1 id="heading">Heading</h1>
      <div class="content">Content 1</div>
      <div class="content">Content 2</div>
    </body>
  </html>
"""


def x():
    print('success')


webview.create_window('Hello world', 'Site/site.html',frameless=False,height=720,width=1440)
webview.start()