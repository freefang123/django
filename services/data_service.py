import pandas as pd

class DataProcessingService:
    """数据处理服务"""
    
    @staticmethod
    def process_student_data():
        """
        处理学生数据示例
        
        Returns:
            dict: 包含原始数据和排序后数据的字典
        """
        data = {
            '姓名': ['张三', '李四', '王五', '赵六'],
            '年龄': [20, 22, 21, 23],
            '性别': ['男', '女', '男', '女'],
            '成绩': [85, 90, 88, 92]
        }

        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 按成绩排序
        df_sorted = df.sort_values(by='成绩', ascending=False)
        
        return {
            'original_data': data,
            'sorted_data': df_sorted.to_dict('records')
        }
    
    @staticmethod
    def analyze_data(data):
        """
        数据分析
        
        Args:
            data (dict): 输入数据
            
        Returns:
            dict: 分析结果
        """
        df = pd.DataFrame(data)
        
        analysis = {
            'total_count': len(df),
            'average_age': df['年龄'].mean() if '年龄' in df.columns else None,
            'average_score': df['成绩'].mean() if '成绩' in df.columns else None,
            'max_score': df['成绩'].max() if '成绩' in df.columns else None,
            'min_score': df['成绩'].min() if '成绩' in df.columns else None,
        }
        
        return analysis 