from flask import request, jsonify
from flask_restx import Resource, Namespace

from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()
# ========== db ==========

connection_string = f"mongodb+srv://{os.getenv('DB_USER')}:1q2w3e4r@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
client = MongoClient(connection_string) # MongoClient 객체 생성

print()
print(client)
print()

db = client['Dashboard']
artists_collection = db['ArtistMeta']

artist_ns = Namespace("Artist")




@artist_ns.route('')
class Artists(Resource): 
    def get(self): 
        # 쿼리 파라미터에서 페이지 번호와 페이지 크기 가져오기 
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # 추가된 쿼리 파라미터
        artist_id = request.args.get('artist_id', default=None, type=int)
        name = request.args.get('name', default=None, type=str)

        # 쿼리 필터링
        query = {}
        if artist_id:
            query['_id'] = int(artist_id)
        if name:
            query['name'] = {'$regex': name, '$options': 'i'}
        


        # 데이터 가져오기
        artists = list(artists_collection.find(query).skip((page - 1) * per_page).limit(per_page))
        total = artists_collection.count_documents(query)

        # 결과를 JSON으로 변환
        result = {
            'total': total,
            'current_page': page,
            'per_page': per_page,
            'artists': {artist['artist_id']: [artist['name'], artist.get('birth')] for artist in artists}
        }

        return jsonify(result)

    def post(self): 
        # 클라이언트가 보낸 JSON 데이터를 가져오기
        data = request.get_json()

        # 데이터 유효성 검증
        required_fields = ['artist_id', 'name', 'birth', 'debut', 'activity', 'artist_type', 'gender', 'artist_genre', 'agency']
        if not all(field in data for field in required_fields):
            return {'message': 'Invalid data'}, 400

        # 데이터베이스에 추가할 데이터 구성
        new_artist = {
            'artist_id': data.get('artist_id'),
            'name': data.get('name'),
            'birth': data.get('birth'),
            'debut': data.get('debut'),
            'activity': data.get('activity'),
            'artist_type': data.get('artist_type'),
            'gender': data.get('gender'),
            'genre': data.get('artist_genre'),
            'agency': data.get('agency')
        }

        # 데이터베이스에 추가
        result = artists_collection.insert_one(new_artist)

        # 추가된 데이터 확인
        if result.acknowledged:
            return {'message': 'Artist added successfully', 'artist': new_artist}, 201
        else:
            return {'message': 'Failed to add artist'}, 500


@artist_ns.route('/<int:artist_id>')
class ArtistSimple(Resource): 
    def get(self, artist_id): # artist_id를 URL 에서 받아온다.  
        artist = artists_collection.find_one({"artist_id": artist_id}) # artist_id로 DB에서 조회한다. 

        if artist is None: 
            return {"message": "Artist not found"}, 404
        
        return {
            "name": artist["name"],
            "birth": artist["birth"],
            "debut": artist["debut"],
            "activity": artist["activity"],
            "artist_type": artist["artist_type"],
            "gender": artist["gender"],
            "agency": artist["agency"],
            "genre": artist["genre"]
        }, 200