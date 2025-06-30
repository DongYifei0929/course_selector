import requests
import json
from typing import List, Dict, Any
from phase1 import get_available_courses,generate_schedule

API_KEY="sk-fd47886700fc43cfa31cf6758f0b4504"

def get_course_recommendations(
    api_key: str,
    available_courses,
    must_take_courses,
    chosen_courses,
    preferences, #{'给分':0,'任务量':0,'早八厌恶程度':0,'选课难度':0,'水分':0}
    your_prompts,
    api_url: str="https://api.deepseek.com/v1/chat/completions"
) -> List[Dict[str,Any]]:
    
    prompt = f"""
    你是一位智能课程推荐助手。根据以下信息，从可选课程列表和可选专业课列表中为用户推荐合适的课程。

    具体来说，用户在各个维度的偏好数值越高表示对该方面要求越高；

    每门课的数据结构形如[记录课程信息的原始字典,[上课时间],[对应维度的课程评分],[限选人数，已选人数]]，其中对应维度的课程评分越高说明该维度表现越好。

    务必注意：

    推荐的课程课名不能和已选课程有重合；

    推荐的课程不能和已有课程产生时间冲突；推荐的课程之间不能有时间冲突；

    可选专业课列表中的课程，相同课名的能且只能选择一门；

    推荐课程和已选课程学分加起来不能超过25分
    
    可选课程列表:
    {json.dumps(available_courses, indent=2)}

    可选专业课列表:
    {json.dumps(must_take_courses, indent=2)}

    已选课程列表:
    {json.dumps(chosen_courses, indent=2)}

    用户个人偏好:
    {json.dumps(preferences, indent=2)}
    
    请返回推荐的课程列表，每个课程的数据结构形如：[记录课程信息的原始字典,[上课时间],[对应维度的课程评分],-1,[限选人数，已选人数],-1]
    注意：不要含有其它任何信息！包括推荐理由、“根据您的需求，我将推荐以下课程”等。要求能够被解析为json格式。
    """
    prompt=prompt+your_prompts
    
    # 构建 API 请求体
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个智能课程推荐助手，根据用户提供的课程列表和个人偏好，为用户推荐合适的课程。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  
        "max_tokens": 1000
    }
    
    try:
        # 发送请求到 DeepSeek API
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        # 解析 API 响应
        api_response = response.json()
        recommendation_text = api_response["choices"][0]["message"]["content"]
        
        try:
            recommended_courses = json.loads(recommendation_text)
        except json.JSONDecodeError:
            print("警告: 无法将推荐结果解析为 JSON，返回原始文本响应")
            recommended_courses = recommendation_text
        
        return recommended_courses
    
    except requests.exceptions.RequestException as e:
        print(f"API 请求错误: {e}")
        return []
    except (KeyError, IndexError) as e:
        print(f"解析 API 响应错误: {e}")
        return []