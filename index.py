from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from os import getenv

app = FastAPI()
# app.mount()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

@app.get('/')#, response_class=HTMLResponse)
async def root(request: Request):
	# return RedirectResponse('/mainpage')
	return templates.TemplateResponse('mainpage.html', {"request": request})

@app.get("/Lapas/favicon.ico", include_in_schema=False)
async def favicon():
	return FileResponse('Lapas/favicon.icon')
@app.get('/static/{attels}')
async def iegūtAttēlu(attels: str):
	# return {'Saņemts': attels}
	# print('mēģināts iegūt attēlu', attēls)
	return FileResponse(f'static/{attels}')
@app.get( "/static/{stils}")
async def iegūtNoformējumu(stils: str):
	return FileResponse(f'static/{stils}')

@app.get('/{lapa_}')
async def izvadītLapu(lapa_:str, request: Request):
	if lapa_=='favicon.ico':
		return FileResponse('Lapas/favicon.ico')
	print('Mēģināts piekļūt lapai:', lapa_)
	sql = 'SELECT * FROM lapas WHERE Title=?;'
	mycursor.execute(sql, (lapa_,))
	fails = mycursor.fetchall()[0][2]
	# with open(f'templates/{lapa_}.html', 'w', encoding='utf-8') as f:
	# 	f.write(fails.replace('\r\n', '\n'))
	return templates.TemplateResponse(f'{lapa_}.html', {"request": request})
