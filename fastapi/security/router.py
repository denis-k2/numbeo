from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import crud
import schemas
import sendmail
from database import get_db

router = APIRouter(tags=["Auth"])


@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    """
    To register, enter **username** (unique) and **password**.
    - **email** - use a real one. You'll get a verification email.
    - **user** - is default role
    - **admin** - application for admin role will be considered individually
    """
    db_user = crud.get_user_by_username(db=db, username=user.username, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User or email already exists in the system"
        )
    db_user = crud.create_user(db=db, user=user)
    token = auth.create_access_token(db_user)
    sendmail.send_mail(to=db_user.email, token=token, username=db_user.username)
    return db_user


@router.post("/login")
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Log in to get a fresh token. Access token expire is 60 minutes.
    """
    db_user = crud.get_user_by_username(db=db, username=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials not correct"
        )

    if auth.verify_password(form_data.password, db_user.hashed_password):
        token = auth.create_access_token(db_user)
        return {"access_token": token, "token_Type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials not correct"
    )


@router.get("/verify/{token}", response_class=HTMLResponse, include_in_schema=False)
def login_user(token: str, db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    username = payload.get("sub")
    db_user = crud.get_user_by_username(db, username)
    db_user.active = True
    db.commit()
    return f"""
    <html>
        <head>
            <title>Registration confirmation</title>
        </head>
        <body>
            <h2>Activation of {username} successful!</h2>
            <a href="http://relohelper.space:8000/docs">
                Back
            </a>
        </body>
    </html>
    """


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    """ test """
    users = crud.get_users(db=db)
    return users


@router.get("/secured", dependencies=[Depends(auth.check_active)])
def get_all_users(db: Session = Depends(get_db)):
    """ test """
    users = crud.get_users(db=db)
    return users


@router.get("/adminsonly", dependencies=[Depends(auth.check_admin)])
def get_all_users(db: Session = Depends(get_db)):
    """ test """
    users = crud.get_users(db=db)
    return users
