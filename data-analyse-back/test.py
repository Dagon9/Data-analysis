import os
from flask import Flask, jsonify, request
import pymysql
import random
from datetime import datetime, timedelta
from flask_cors import CORS  # 添加跨域支持
import requests



app = Flask(__name__)
CORS(app)  # 允许所有域的跨域请求

# 数据库配置（本地）
#DB_CONFIG = {
#   "host": "localhost",  # 移除端口号
#    "port": 3306,         # 添加独立端口配置
#    "user": "root",       # 添加双引号保持键一致性
#    "password": "123456",
#    "database": "news_db",
#    "charset": "utf8mb4"
#}
# 数据库配置（彬）
DB_CONFIG = {
    "host": "192.168.2.205",  # 移除端口号
    "port": 3306,         # 添加独立端口配置
    "user": "root",       # 添加双引号保持键一致性
    "password": "000000",
    "database": "analyse",
    "charset": "utf8mb4"
}

#数据库链接检查
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route("/db-check")
def db_check():
    try:
        conn = get_db_connection()
        conn.ping()
        return "Database connection successful!"
    except Exception as e:
        return f"Connection failed: {str(e)}", 500


#新闻原始数据插入
@app.route("/api/insert-news", methods=["POST"])
def handle_news_insert():
    """接收其他后端服务的新闻数据插入请求"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['title', 'content', 'media_name', 'publish_time', 'author']
        for item in data:
            if not all(field in item for field in required_fields):
                return jsonify({
                    "status": "error",
                    "message": f"缺失必要字段，需要包含：{', '.join(required_fields)}"
                }), 400
        
        # 调用批量插入函数
        result = batch_insert_news_raw(data)
        if result['status'] == 'success':
            return jsonify({
                "status": "success",
                "inserted_count": result['inserted'],
                "timestamp": datetime.now().isoformat()
            })
        return jsonify(result), 500
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"请求处理失败: {str(e)}"
        }), 500

# 在新闻统计函数前添加批量插入函数
def batch_insert_news_raw(data_list):
    """批量插入新闻原始数据"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 使用与表结构匹配的插入语句（自动递增ID不需要插入）
            sql = """INSERT INTO news_raw_data 
                    (title, content, media_name, publish_time, author, crawl_time)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            
            # 构造参数列表（自动生成爬取时间）
            params = [(item['title'], item['content'], item['media_name'],
                      item['publish_time'], item['author'], datetime.now()) 
                     for item in data_list]
            
            cursor.executemany(sql, params)
            conn.commit()
            return {"status": "success", "inserted": len(data_list)}
            
    except pymysql.Error as e:
        conn.rollback()
        return {"status": "error", "message": f"数据库操作失败: {str(e)}"}
    finally:
        if conn:
            conn.close()



# 新闻统计核心逻辑
def news_statistics():
    stats = {}
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 统计总新闻数
            cursor.execute("SELECT COUNT(*) FROM news")
            stats['total'] = cursor.fetchone()[0]
            
            # 统计最近7天每日新闻数
            cursor.execute("""
                SELECT DATE(publish_date) as date, COUNT(*) 
                FROM news 
                WHERE publish_date >= %s
                GROUP BY date
                ORDER BY date DESC
            """, (datetime.now() - timedelta(days=7),))
            stats['by_date'] =  {str(date): count for date, count in cursor.fetchall()}
            
            # 统计新闻分类分布
            cursor.execute("""
                SELECT category, COUNT(*) 
                FROM news 
                GROUP BY category 
                ORDER BY COUNT(*) DESC
            """)
            stats['by_category'] = dict(cursor.fetchall())
            print(stats)
        return stats
    finally:
        connection.close()

@app.route("/api/stats")
def get_stats():
    return jsonify({
        "status": "success",
        "data": news_statistics(),
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/hot-topics")
def get_hot_topics():
    # 生成20条示例数据
    sample_topics = [
        "人工智能监管政策出台",
        "新能源汽车价格战",
        "元宇宙技术新突破",
        "全球芯片短缺持续",
        "加密货币市场波动",
        "量子计算新进展",
        "气候变化国际会议",
        "跨境电商新规实施",
        "太空探索新计划",
        "基因编辑技术突破"
    ]
    
    hot_topics = [{
        "topic": f"{random.choice(sample_topics)}",
        "heat": random.randint(1000, 100000)
    } for i in range(20)]
    
    # 按热度降序排序
    hot_topics.sort(key=lambda x: x["heat"], reverse=True)
    
    return jsonify({
        "status": "success",
        "data": {
            "hot_topics": hot_topics,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@app.route("/api/keywords")
def get_keywords():
    # 生成20条关键词示例数据
    base_keywords = [
        "人工智能", "区块链", "元宇宙", "碳中和", "数字货币",
        "量子计算", "基因编辑", "自动驾驶", "5G通信", "物联网",
        "边缘计算", "虚拟现实", "机器学习", "数据安全", "云计算",
        "生物科技", "智慧城市", "数字化转型", "工业互联网", "芯片制造"
    ]
    
    keywords_data = [{
        "keyword": f"{kw}{i+1}",  # 添加序号区分相同关键词
        "count": random.randint(100, 10000)
    } for i, kw in enumerate(random.choices(base_keywords, k=20))]
    
    # 按出现次数降序排序
    keywords_data.sort(key=lambda x: x["count"], reverse=True)
    
    return jsonify({
        "status": "success",
        "data": {
            "keywords": keywords_data,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@app.route("/api/topic-click", methods=["POST"])
def handle_topic_click():
    try:
        # 获取前端发送的话题数据
        topic_data = request.json
        print(f"收到话题点击: {topic_data.get('topic', '未知话题')}")
        
        # 预定义模拟数据组件
        titles = [
            "行业动态分析报告", 
            "最新政策解读", 
            "专家观点汇总",
            "技术创新追踪",
            "市场趋势预测"
        ]
        authors = ["王", "李", "张", "刘", "陈"]
        sources = ["新华网", "人民网", "腾讯新闻", "新浪财经", "澎湃新闻"]
        keywords = ["政策", "经济", "技术", "市场", "创新"]
        summaries = [
            "近期行业动态显示相关领域发展迅速，多家企业推出创新产品。",
            "专家认为该趋势将对市场格局产生深远影响，值得持续关注。",
            "最新政策文件明确了行业发展方向，提出多项扶持措施。"
        ]
        
        # 生成3条模拟新闻数据
        related_news = []
        for _ in range(3):
            related_news.append({
                "title": f"{topic_data.get('topic', '热点')}：{random.choice(titles)}",
                "author": f"{random.choice(authors)}研究员",
                "source": random.choice(sources),
                "keywords": ", ".join(random.sample(keywords, 3)),
                "summary": random.choice(summaries)
            })
        
        return jsonify({
            "status": "success",
            "data": {
                "original_topic": topic_data,
                "related_news": related_news
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"处理失败: {str(e)}"
        }), 500

@app.route("/api/generate-article", methods=["POST"])
def generate_article():
    try:
        data = request.get_json()
        # 强化参数验证
        required_fields = ['title', 'author', 'source']
        if not all(field in data for field in required_fields):
            return jsonify({
                "status": "error",
                "message": f"缺少必要字段: {', '.join(required_fields)}"
            }), 400

        # 移除数据库相关代码
        article_template =    """
            {title}
            {author} | {source}

            近日，关于的报道引发广泛关注。随着科技发展，该领域持续创新。行业专家表示，这一突破将带来三方面影响：

            1. 推动相关产业链升级：产业链上下游企业将加速技术迭代，预计带动超过200家配套企业发展。
            2. 创造新的就业机会：初步估算将在未来三年内新增10万个相关岗位，涉及研发、生产、运维等多个领域。
            3. 促进跨领域技术融合：该技术将与人工智能、大数据分析等技术结合，形成复合型解决方案。

            据统计数据显示，该领域近三年增长率保持在15%以上，主要应用场景包括：
            - 智能制造生产线：已在30余家大型制造企业部署应用
            - 智慧城市建设：成功落地5个省级智慧城市试点项目
            - 数字经济发展：带动相关产业规模突破5000亿元

            技术突破还体现在：
            * 研发投入同比增长45%
            * 专利申请量较去年同期增长60%
            * 产学研合作项目数量翻番

            未来发展趋势将聚焦人工智能与大数据技术的深度融合。行业领军企业计划在未来五年内投入50亿元研发资金，重点突破核心技术瓶颈。市场分析指出，该领域有望在2030年前形成万亿级市场规模，成为经济增长新引擎。"""# 保持原有模板不变
        
        # 合并处理逻辑，移除重复的请求处理
        formatted_content = article_template.format(
            title=data['title'],
            author=data['author'],
            source=data['source']
        )

        return jsonify({
            "status": "success",
            "data": {  # 保持数据结构与前端匹配
                "content": formatted_content,
                "word_count": len(formatted_content)
            }
        })
        
    except KeyError as e:
        return jsonify({
            "status": "error",
            "message": f"参数格式错误: 缺少 {str(e)} 字段"
        }), 400
    except Exception as e:
        app.logger.error(f"文章生成失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "内容生成服务暂时不可用",
            "error_detail": str(e)
        }), 500

@app.route("/api/chat", methods=["POST"])
def chat_handler():
    try:
        data = request.get_json()
        context = data.get('context', '')[:2000]

        #api_key = os.getenv("DEEPSEEK_API_KEY")
        api_key = "sk-0e217b08ae844958b6448b3c539f547f"
        # 替换为DeepSeek API调用
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key.strip()}"
        }
        
        # 改进的请求参数
        payload = {
            "model": "deepseek-chat",  # 更新模型版本
            "messages": [
                {
                    "role": "system",
                    "content": f"请基于以下新闻内容回答问题：{context}"  # 更明确的指令
                },
                {
                    "role": "user",
                    "content": data.get('message', '')[:500]  # 添加用户消息内容
                }
            ],
            "temperature": 0.3,  # 降低随机性
            "max_tokens": 800,
            "top_p": 0.9
        }
        
        # 增强错误处理
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15  # 延长超时时间
        )
                # 增强错误处理（添加状态码检查）
        if response.status_code >= 400:
            app.logger.error(f"API请求失败 | 状态码：{response.status_code} | 响应：{response.text}")
        
        response_data = response.json()
        
        # 更健壮的错误解析
        if 'error' in response_data:
            error_msg = response_data['error'].get('message', '未知错误')
            error_code = response_data['error'].get('code', -1)
            raise Exception(f"API错误({error_code}): {error_msg}")
            
        # 添加空响应校验
        if not response_data.get('choices'):
            raise ValueError("API返回结构异常")
        answer = response_data['choices'][0]['message']['content']
        
        return jsonify({
            "status": "success",
            "data": {
                "answer": answer,
                "suggestions": ["技术解析", "数据验证", "行业影响"]
            }
        })
        
    except Exception as e:
        app.logger.error(f"DeepSeek API错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "智能问答服务暂时不可用",
            "error_detail": str(e)[:100]
        }), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

