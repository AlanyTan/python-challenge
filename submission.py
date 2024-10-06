"""server app for serving challenge page and check results"""
import os
import json
from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from config import config
from utils import challenge_details, logger_contextman
import check_submission

templates = Jinja2Templates(directory="static")

app = FastAPI()

logger = logger_contextman.get_logger(__name__, 'DEBUG')


@app.get("/")
async def root_redirect() -> RedirectResponse:
    """redicrect root to selector page"""
    return RedirectResponse("/challenges/", 301)


class Submission(BaseModel):
    """the type for browser submit code"""
    code: str


@app.get("/challenges/{challenge_id:path}", response_class=HTMLResponse)
async def read_challenge(request: Request, challenge_id: str) -> HTMLResponse:
    """return the page of the given challenge. challenge_id must exist"""
    challenge_dir = os.path.join(config.CHALLENGE_DIR, challenge_id)

    if os.path.isdir(challenge_dir):
        try:
            challenge_data = challenge_details(challenge_id)
            if challenge_data and (cc := challenge_data.get('condition_code')):
                cc = f"#### Do not change this section ##### \n{cc}"
                cc += "##### End do-not-change section #####\n\n"
                sc = cc + challenge_data.get("starting_code", '')
            else:
                sc = challenge_data.get("starting_code", '')

            return templates.TemplateResponse("challenge.html", {
                "request": request,
                "challenge_id": challenge_id,
                "title": challenge_data.get("title"),
                "description": challenge_data.get("description"),
                "notes": challenge_data.get("notes"),
                "goal": challenge_data.get("goal"),
                "starting_code": sc,
            })
        except FileNotFoundError as e:
            logger.debug("%s is not a leaf challenge node, (%s), "
                         "showing listdir content as list...", challenge_id, e)
            sub_challenges = []
            for subdir in sorted(os.listdir(challenge_dir)):
                subdir_path = os.path.join(challenge_dir, subdir)
                if not os.path.isdir(subdir_path):
                    continue
                description = ""
                problem_file = os.path.join(
                    subdir_path, config.PROBLEM_FILENAME)
                if os.path.isfile(problem_file):
                    with open(problem_file, encoding='utf-8') as f:
                        problem_data = json.load(f)
                        description = problem_data.get("title", "")
                else:
                    for subsubdir in sorted(os.listdir(subdir_path)):
                        if os.path.isdir(os.path.join(subdir_path, subsubdir)):
                            description += (", " if description else ""
                                            ) + subsubdir
                    description = f"multiple challenges: ({description})."
                sub_challenges.append({
                    "name": subdir,
                    "description": description,
                    "url": f"/challenges/{challenge_id}"
                    f"{'/' if challenge_id else ''}{subdir}"
                })
            return templates.TemplateResponse("sub_challenges.html", {
                "request": request,
                "challenge_id": challenge_id,
                "sub_challenges": sub_challenges
            })
        except Exception as e:
            logger.warning("Opening challenge file run into Error:%s", e)

    else:
        logger.error("%s is not a valid challenge dir.", challenge_id)
        return HTMLResponse(f"Challenge {challenge_id} not found.",
                            status_code=404)


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
        logger.error("check_submission run into Error %s", e)
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
        f.write(f"{user_id},{problem_id},{output=}. Error:{error=}\n")

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
    with logger_contextman.logging_context(__name__, 'DEBUG') as logger:
        uvicorn.run(app, host=config.HOST, port=config.PORT)
