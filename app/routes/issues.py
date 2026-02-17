import uuid
from fastapi import APIRouter, HTTPException, status
from app.storage import load_data, save_data
from app.schemas import IssueCreate, IssueUpdate, IssueOut, IssueStatus
 

router = APIRouter(prefix='/api/v1/issues',tags=['Issues'])

@router.get("/", response_model=list[IssueOut])
async def get_issues():
    '''Retrieve all issues.'''
    issues = load_data()
    return issues

@router.get('/{issue_id}', response_model=IssueOut)
def get_issue_with_id(issue_id: str):
    '''Retrieve issue with the issue id'''
    issues = load_data()
    for issue in issues:
        if issue['id'] == issue_id:
            return issue
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found")


@router.post("/", response_model=IssueOut,status_code=status.HTTP_201_CREATED)
async def create_issue(payload : IssueCreate):
    '''Create a new issue'''
    issues = load_data()
    new_issue = {
        'id': str(uuid.uuid4()),
        'title': payload.title,
        'description': payload.description,
        'priority': payload.priority,
        'status': IssueStatus.open
    }
    issues.append(new_issue)
    save_data(issues)
    return new_issue

@router.put('/{issue_id}', response_model=IssueOut)
def update_issue(issue_id: str, payload: IssueUpdate):
    '''Updating the existing issue with issue id'''
    issues = load_data()
    for index, issue in enumerate(issues):
        if issue['id'] == issue_id:
            if payload.title is not None: issues[index]['title'] = payload.title
            if payload.description is not None: issues[index]['description'] = payload.description
            if payload.priority is not None: issues[index]['priority'] = payload.priority
            if payload.status is not None: issues[index]['status'] = payload.status
            save_data(issues)
            return issues[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Issue not found"
    )

@router.delete('/{issue_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id:str):
    '''Deleting issue with issue id'''
    issues = load_data()
    for index, issue in enumerate(issues):
       if issue['id'] == issue_id:
           issues.pop(index)
           save_data(issues)
           return
       
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Issue not found')

