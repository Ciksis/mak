from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
# app.mount()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

@app.get('/')#, response_class=HTMLResponse)
async def root(request: Request):
	# return RedirectResponse('/mainpage')
	return templates.TemplateResponse('mainpage.html', {"request": request})
@app.get('/ATLANT')#, response_class=HTMLResponse)
async def root1(request: Request):
	return templates.TemplateResponse('ATLANT.html', {"request": request})
@app.get('/TITAN-PRO')#, response_class=HTMLResponse)
async def root2(request: Request):
	return templates.TemplateResponse('TITAN-PRO.html', {"request": request})
@app.get('/KRONOS')#, response_class=HTMLResponse)
async def root3(request: Request):
	return templates.TemplateResponse('KRONOS.html', {"request": request})
@app.get('/ODESSEY')#, response_class=HTMLResponse)
async def root4(request: Request):
	return templates.TemplateResponse('ODESSEY.html', {"request": request})
@app.get('/contacts')#, response_class=HTMLResponse)
async def root5(request: Request):
	return templates.TemplateResponse('contacts.html', {"request": request})
@app.get('/mezu-kopsana')#, response_class=HTMLResponse)
async def root6(request: Request):
	return templates.TemplateResponse('mezu-kopsana.html', {"request": request})
@app.get('/login')#, response_class=HTMLResponse)
async def root7(request: Request):
	return templates.TemplateResponse('login.html', {"request": request})


# @app.get("/static/favicon.ico", include_in_schema=False)
# async def favicon():
# 	return FileResponse('static/favicon.icon')
@app.get('/static/{attels}')
async def iegūtAttēlu(attels: str):
	# return {'Saņemts': attels}
	# print('mēģināts iegūt attēlu', attēls)
	return FileResponse(f'static/{attels}')
@app.get( "/static/{stils}")
async def iegūtNoformējumu(stils: str):
	return FileResponse(f'static/{stils}')

# @app.get('/{lapa_}')
# async def izvadītLapu(lapa_:str, request: Request):
# 	if lapa_=='favicon.ico':
# 		return FileResponse('Lapas/favicon.ico')
# 	print('Mēģināts piekļūt lapai:', lapa_)
# 	sql = 'SELECT * FROM lapas WHERE Title=?;'
# 	mycursor.execute(sql, (lapa_,))
# 	fails = mycursor.fetchall()[0][2]
# 	# with open(f'templates/{lapa_}.html', 'w', encoding='utf-8') as f:
# 	# 	f.write(fails.replace('\r\n', '\n'))
# 	return templates.TemplateResponse(f'{lapa_}.html', {"request": request})

if __name__ == "__main__":
	uvicorn.run("index:app", host="0.0.0.0", port=443, ssl_keyfile="/etc/letsencrypt/live/mak-3.com/privkey.pem", ssl_certfile="/etc/letsencrypt/live/mak-3.com/fullchain.pem")