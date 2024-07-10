from typing import Any

from fastapi import APIRouter, HTTPException
from starlette import status

from app import crud
from app.api.dependencies import SessionDep, CurrentUser
from app.models import SubmissionCreate, Submission, SubmissionPublic, SubmissionsPublic

router = APIRouter()


@router.post("/{problem_id}/judge")
def create_submission(session: SessionDep, current_user: CurrentUser, submission_in: SubmissionCreate, problem_id: int) -> Any:
    """
    수업 내에서 문제 채점(submission 생성)
    """
    submission = crud.create_submission(session=session,
                                        submission_in=submission_in,
                                        user_id=current_user.id,
                                        course_problem_id=problem_id)
    return submission


@router.get("/result", response_model=SubmissionsPublic)
def read_submission_list(session: SessionDep,
                         student_id: str | None,
                         course_id: int | None,
                         problem_id: int | None):
    """
    문제 채점 결과 목록(제출id, ) 검색 가능: 검색용 쿼리 매개변수
    """
    #TODO
    #TODO 페이징 추가 필요
    pass


@router.get("/{submission_id}/source", response_model=SubmissionPublic)
def read_my_source(session: SessionDep, current_user: CurrentUser, submission_id: int):
    """
    제출 코드 확인(교수, 학생), 제출자 본인이거나 교수자 아니면 확인 불가
    """
    submission = session.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="not found")

    if not submission.submitter_id == current_user.student_id or current_user.is_professor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to read this")

    return submission


#TODO 문제 채점 결과(로그, 교수)