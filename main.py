from typing import List, Optional, Tuple
import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.logger import logger as fastapi_logger
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

logger = logging.getLogger("uvicorn")
fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)
logger.error("API Started")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/movies/", response_model=List[schemas.Movie])
def read_movies(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    # read items from database
    movies = crud.get_movies(db, skip=skip, limit=limit)
    # return them as json
    return movies

@app.post("/movies/", response_model=schemas.Star)
def make_movie(star: schemas.MovieCreate, db: Session = Depends(get_db)):
	return crud.create_star(db=db, star=star)


@app.put("/movies/", response_model=schemas.Movie)
def update_movie(movie: schemas.Movie, db: Session = Depends(get_db)):
    db_movie = crud.update_movie(db=db, movie=movie)
    if db_movie is None:
    	raise HTTPException(status_code=404, detail="Movie to update not found")
    return db_movie

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def dlt_movie(movie_id: int, db: Session = Depends(get_db)):
	db_movie = crud.dlt_movie(db=db, movie_id=movie_id)
	if db_movie is None:
		raise HTTPException(status_code=404, detail="Movie to delete not found")
	return db_movie


@app.put("/movies/director/", response_model=schemas.MovieDetail)
def update_movie_director(mid: int, sid: int, db: Session = Depends(get_db)):
    db_movie = crud.update_movie_director(db=db, movie_id=mid, director_id=sid)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star not found")
    return db_movie

@app.post("/movies/actor/", response_model=schemas.MovieDetail)
def add_movie_actor(mid: int, sid: int, db: Session = Depends(get_db)):
	db_movie = crud.add_movie_actor(db=db, movie_id=mid, star_id=sid)
	if db_movie is None:
		raise HTTPException(status_code=404, detail="Movie or Star not found")
	return db_movie

@app.put("/movies/actors/", response_model=schemas.MovieDetail)
def update_movie_actors(mid: int, sids: List[int], db: Session = Depends(get_db)):
	db_movie = crud.replace_movie_actors(db=db, mid=mid, sids=sids)
	if db_movie is None:
	    raise HTTPException(status_code=404, detail="Movie or Star not found")
	return db_movie



@app.get("/movies/by_id/{movie_id}", response_model=schemas.MovieDetail)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie to read not found")
    return db_movie

@app.get("/movies/by_title", response_model=List[schemas.Movie])
def read_movies_by_title(t: str, db: Session = Depends(get_db)):
    return crud.get_movies_by_title(db=db, title=t)
            
@app.get("/movies/by_title_part", response_model=List[schemas.Movie])
def read_movies_by_title_part(t: str, db: Session = Depends(get_db)):
    return crud.get_movies_by_title_part(db=db, title=t)
    # Exeemple de Fake returns
    # return [schemas.Movie(title='Mulan', year=1998, id=1)]
    # return [{'title':'Mulan','year':1998, 'id':1}]

@app.get("/movies/by_year/{year}", response_model=List[schemas.Movie])
def read_movies_by_year(year: int, db: Session = Depends(get_db)):
    return crud.get_movies_by_year(db=db, year=year)

@app.get("/movies/by_range_year", response_model=List[schemas.Movie])
def read_movies_by_range_year(ymin: Optional[int], ymax: Optional[int], db: Session = Depends(get_db)):
    return crud.get_movies_by_range_year(db=db, year_min=ymin, year_max=ymax)

@app.get("/movies/by_title_year", response_model=List[schemas.Movie])
def read_movies_by_title_year(t: str, y: int, db: Session = Depends(get_db)):
    return crud.get_movies_by_title_year(db=db, title=t, year=y)

@app.get("/movies/count")
def read_movies_count(db: Session = Depends(get_db)):
    return crud.get_movies_count(db=db)

@app.get("/movies/count/{year}")
def read_movies_count_year(year:int, db: Session = Depends(get_db)):
    return crud.get_movies_count_year(db=db, year=year)

@app.get("/movies/by_director", response_model=List[schemas.Movie])
def read_movies_by_director(n: str, db: Session = Depends(get_db)):
    return crud.get_movies_by_director_endname(db=db, endname=n)

@app.get("/movies/by_actor", response_model=List[schemas.Movie])
def read_movies_by_actor(n: str, db: Session = Depends(get_db)):
    return crud.get_movies_by_actor_endname(db=db, endname=n)

@app.get("/movies/count_by_year")
def read_count_movies_by_year(db: Session = Depends(get_db)) -> List[Tuple[int, int]]:
    return crud.get_movies_count_by_year(db=db)


# --- API Rest for Stars ---
    
@app.get("/stars/", response_model=List[schemas.Star])
def read_stars(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    stars = crud.get_stars(db, skip=skip, limit=limit)
    return stars

@app.post("/stars/", response_model=schemas.Star)
def make_star(star: schemas.StarCreate, db: Session = Depends(get_db)):
	return crud.make_star(db=db, star=star)    

@app.put("/stars/", response_model=schemas.Star)
def update_star(star: schemas.Star, db: Session = Depends(get_db)):
	db_star = crud.update_star(db=db, star=star)
	if db_star is None:
		raise HTTPException(status_code=404, detail="Star to update not found")
	return db_star

@app.delete("/stars/{star_id}", response_model=schemas.Star)
def dlt_star(movie_id: int, db: Session = Depends(get_db)):
	db_star = crud.dlt_star(db=db, movie_id=movie_id)
	if db_star is None:
		raise HTTPException(status_code=404, detail="Star to delete not found")
	return db_star


@app.get("/stars/by_id/{star_id}", response_model=schemas.Star)
def read_star(star_id: int, db: Session = Depends(get_db)):
    db_star = crud.get_star(db, star_id=star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="Star to read not found")
    return db_star

@app.get("/stars/by_name", response_model=List[schemas.Star])
def read_stars_by_name(n: str, db: Session = Depends(get_db)):
    # read items from database
    stars = crud.get_stars_by_name(db=db, name=n)
    return stars

@app.get("/stars/by_endname", response_model=List[schemas.Star])
def read_stars_by_endname(n: str, db: Session = Depends(get_db)):
    # read items from database
    stars = crud.get_stars_by_endname(db=db, name=n)
    return stars

@app.get("/stars/by_birthyear/{year}", response_model=List[schemas.Star])
def read_stars_by_birthyear(year: int, db: Session = Depends(get_db)):
    # read items from database
    stars = crud.get_stars_by_birthyear(db=db, year=year)
    return stars

@app.get("/stars/count")
def read_stars_count(db: Session = Depends(get_db)):
    return crud.get_stars_count(db=db)

@app.get("/stars/by_movie_directed/{movie_id}", response_model=Optional[schemas.Star])
def read_stars_by_movie_directed_id(movie_id: int, db: Session = Depends(get_db)):
    return crud.get_star_director_movie(db=db, movie_id=movie_id)
    # return None if movie has no director (normal) or if movie doesn't exist (error) 
    
@app.get("/stars/by_movie_directed_title/", response_model=List[schemas.Star])
def read_stars_by_movie_directed_title(t: str, db: Session = Depends(get_db)):
    return crud.get_star_director_movie_by_title(db=db, title=t)   

@app.get("/stars/stats_movie_by_director", response_model=List[schemas.DirectorStat])
def read_stats_movies_by_director(minc: Optional[int] = 10, db: Session = Depends(get_db)) -> List[Tuple[schemas.Star, int]]:
    return crud.get_stats_movie_by_director(db=db, min_count=minc)

@app.get("/stars/stats_by_actors/", response_model=List[schemas.StarStat])
def read_stats_actors(minc: Optional[int] = 5, db: Session = Depends(get_db)):
    db_stats = crud.get_stats_by_actors(db=db, min_count=minc)
    return db_stats
