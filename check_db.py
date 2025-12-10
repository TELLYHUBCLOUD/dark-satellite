from models import Question, db_manager

def check_counts():
    try:
        db_manager.connect()
        print("Total Questions:", Question.count())
        print("Subjects:", Question.get_subjects())
        
        for subject in Question.get_subjects():
            count = len(Question.get_random_by_subject(subject, 1000))
            print(f"Subject: {subject}, Count: {count}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_counts()
