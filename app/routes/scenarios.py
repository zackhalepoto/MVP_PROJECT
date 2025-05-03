from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Scenario, ScenarioStep
from app.services.tts import generate_tts
from app.services.synthflow import generate_text_from_synthflow
import json

scenarios_bp = Blueprint('scenarios', __name__)

@scenarios_bp.route('/scenarios', methods=['POST'])
@jwt_required()
def create_scenario():
    data = request.get_json()
    title = data.get('title')
    user_data = json.loads(get_jwt_identity())
    user_id = user_data['id']

    scenario = Scenario(title=title, user_id=user_id)
    db.session.add(scenario)
    db.session.commit()
    return jsonify({'msg': 'Scenario created', 'id': scenario.id})

@scenarios_bp.route('/scenarios', methods=['GET'])
@jwt_required()
def list_scenarios():
    user_data = json.loads(get_jwt_identity())
    user_id = user_data['id']
    scenarios = Scenario.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': s.id, 'title': s.title, 'created_at': s.created_at.isoformat()} for s in scenarios])

@scenarios_bp.route('/scenarios/<int:scenario_id>/steps', methods=['POST'])
@jwt_required()
def add_step(scenario_id):
    data = request.get_json()
    text = data.get('text')
    user_data = json.loads(get_jwt_identity())
    user_id = user_data['id']

    scenario = Scenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    if not scenario:
        return jsonify({'msg': 'Scenario not found'}), 404

    try:
        audio_url = generate_tts(text)
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

    step = ScenarioStep(scenario_id=scenario_id, text=text, audio_url=audio_url)
    db.session.add(step)
    db.session.commit()
    return jsonify({'msg': 'Step added with audio', 'step_id': step.id, 'audio_url': audio_url})

@scenarios_bp.route('/scenarios/<int:scenario_id>/steps', methods=['GET'])
@jwt_required()
def list_steps(scenario_id):
    user_data = json.loads(get_jwt_identity())
    user_id = user_data['id']
    scenario = Scenario.query.filter_by(id=scenario_id, user_id=user_id).first()
    if not scenario:
        return jsonify({'msg': 'Scenario not found'}), 404

    steps = ScenarioStep.query.filter_by(scenario_id=scenario_id).all()
    return jsonify([{'id': step.id, 'text': step.text, 'audio_url': step.audio_url} for step in steps])

@scenarios_bp.route('/synthflow/generate-step', methods=['POST'])
@jwt_required()
def generate_step_with_ai():
    data = request.get_json()
    prompt = data.get('prompt')

    try:
        generated_text = generate_text_from_synthflow(prompt)
        return jsonify({'generated_text': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500