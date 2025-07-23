import uvicorn
import pathlib

if __name__ == '__main__':
    uvicorn.run('rvc.api_240604:app', host='127.0.0.1', port=8765, log_level='info')
