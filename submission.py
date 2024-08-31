"""server app for serving challenge page and check results"""
import os
import json
from fastapi import FastAPI, Header, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config import config
import check_submission

templates = Jinja2Templates(directory="static")

app = FastAPI()


@app.get("/")
async def root_redirect() -> RedirectResponse:
    """redicrect root to selector page"""
    return RedirectResponse("/challenges/123", 301)


class Submission(BaseModel):
    """the type for browser submit code"""
    code: str


@app.get("/challenges/{challenge_id}", response_class=HTMLResponse)
async def read_challenge(request: Request, challenge_id: str):
    """return the page of the given challenge. challenge_id must exist"""
    # Load challenge data from JSON file
    with open(f"{config.CHALLENGE_DIR}/{challenge_id}/problem.json",
              encoding='utf-8') as f:
        challenge_data = json.load(f)

    return templates.TemplateResponse("challenge.html", {
        "request": request,
        "challenge_id": challenge_id,
        "title": challenge_data.get("title"),
        "description": challenge_data.get("description"),
        "notes": challenge_data.get("notes"),
        "goal": challenge_data.get("goal"),
        "starting_code": challenge_data.get("starting_code"),
    })


@app.post("/submission")
async def execute_code(submission: Submission, user_id: str = Header(None),
                       problem_id: str = Header(None)) -> JSONResponse:
    """accept submission and test it"""
    code = submission.code
    tmp_file_name = os.path.join(
        config.USER_SUBMISSION_DIR, user_id, f"{problem_id}.py")
    os.makedirs(os.path.dirname(tmp_file_name), exist_ok=True)

    # Create a temporary Python file
    with open(tmp_file_name, "w", encoding='utf-8') as f:
        f.write(code)

    # Execute the code in a separate Python session
    try:
        output = check_submission.check_submission(problem_id, tmp_file_name)
        error = ""
    except Exception as e:
        output = ""
        error = str(e)

    # Return the execution result as a JSON response
    response = {
        "user_id": user_id,
        "problem_id": problem_id,
        "output": output,
        "error": error
    }
    with open("result.csv", 'a+', encoding='utf-8') as f:
        f.write(f"{user_id},{problem_id},{output}. Error:{error}\n")

    return JSONResponse(content=response)


@app.get("/results")
async def get_results() -> JSONResponse:
    """return the content of submission evaluation history for all users."""
    results = []
    with open("result.csv", 'r', encoding='utf-8') as f:
        for line in f:
            user_id, problem_id, *output_error = line.strip().split(',')
            results.append({
                "user_id": user_id,
                "problem_id": problem_id,
                "output": output_error
            })
    return JSONResponse(content=results)

app.mount("/", StaticFiles(directory="static"), name="static")

# Run the FastAPI server on port 3000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
