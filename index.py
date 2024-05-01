from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from os import getenv
import mysql.connector
db = mysql.connector.connect(
	host=getenv("DB_HOST"),
	user=getenv("DB_USER"),
	port=getenv("DB_PORT"),
	password=getenv("DB_PASSWORD"),
	database=getenv("DB_NAME")
)

mycursor = db.cursor(prepared=True)

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

@app.get('/admin')
async def admin_login(wrong:bool = False):
	'''wrong - ja True, tad ir ticis atsūtīts no citas lapas un parole nav pareiza'''
	with open('admin.html', 'r', encoding='utf-8') as f:
		lapa = f.read()
		if wrong:
			meklēt = '<div class="kluda"></div>'
			i = lapa.index(meklēt)
			lapa = lapa.replace(meklēt,
				'<div class="kluda">Lietotājvārds un/vai parole nav pareiza</div>'
			)
		return HTMLResponse(lapa)
	
@app.post('/admin/log')
async def log_pārbaude(lietotajs: str = Form(), parole: str = Form()):
	if lietotajs=='admin' and parole=='admin':
		return RedirectResponse('/admin/lapas')
	return RedirectResponse('/admin?wrong=1', status_code=303)

@app.post('/admin/lapas')
async def lapu_aps(request:Request):
	mycursor.execute('SELECT * FROM lapas')
	lapas = mycursor.fetchall()

	return templates.TemplateResponse('_lapas.html', {"request": request, 'lapas':lapas})
	
@app.post('/admin/lapas/{lapas_id}')
async def lapas_red(lapas_id: int, request: Request):
	# return f'Rediģējam lapu {lapas_id}'

	mycursor.execute(f'SELECT Title, Fails FROM lapas WHERE lapasID=?', (lapas_id,))
	tituls, fails  = mycursor.fetchall()[0]

	return templates.TemplateResponse('_el_red.html', {"request": request, 'lapas_id':lapas_id, 'tituls':tituls, 'fails':fails})
	
@app.post('/admin/atjaunotV')
async def atjaunotV(title:str = Form(), lapaID:str= Form(), fails: str=Form()):
	# return (title, lapaID, len(fails))
	sql = '''UPDATE lapas SET Title = ?, Fails = ? WHERE LapasID=?'''
	mycursor.execute(sql, (title, fails, lapaID))
	db.commit()
	return RedirectResponse(f'/admin/lapas')

@app.post('/registresanas')
async def reģistrēties(request: Request, vards:str = Form(), epasts:str = Form(), parole:str = Form(),):
	sql = 'SELECT * FROM lietotaji WHERE epasts=?'
	mycursor.execute(sql, (epasts,))
	rezultāts = mycursor.fetchall()
	if len(rezultāts)==0:#Sanāca
		sql = 'INSERT INTO lietotaji (Vards, epasts, parole) VALUES (?, ?, ?);'
		mycursor.execute(sql, (vards, epasts, parole))
		db.commit()

		return RedirectResponse('/', status_code=303)#'Jauns konts'
	else:
		return RedirectResponse('/login?pastav=1', status_code=303)
		# return templates.TemplateResponse('login.html', {'request':request, 'active':'active'})
		# return 'Eksistē e-pasts'

	

@app.post('/ielogosanas')
async def ielogoties(epasts:str = Form(), parole:str =Form(), atcereties =Form()):
	sql = 'SELECT * FROM lietotaji WHERE epasts=?'
	mycursor.execute(sql, (epasts,))
	īstais = mycursor.fetchall()
	print(īstais)
	return epasts, parole, atcereties


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
