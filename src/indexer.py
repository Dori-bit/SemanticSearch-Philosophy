import pandas as pd
import wikipedia
import os

def wiki_corpus():
    """
    Автоматически собирает корпус текстов из русской Википедии. Проходит по списку тем, чистит текст и разбивает его на абзацы.
    """
    wikipedia.set_lang("ru")

    """ 
    Можно добавить что-то свое при желании
    """
    
    topics = [
        "Платон", "Иммануил Кант", "Фридрих Ницше", "Экзистенциализм", "Смысл жизни", "Этика", "Метафизика", "Сократ", "Аристотель", "Нигилизм"
    ]

    doc = []

    for t in topics:
        try:
            page = wikipedia.page(t)
            parag = page.content.split('\n')

            for p in parag:
                clean_p = p.strip()
                
                if len(clean_p) > 150 and not clean_p.startswith('=='):
                    doc.append({
                        'book': t,
                        'text': clean_p
                    })
        except Exception as e:
            print(f"Ошибка при загрузке '{t}': {e}")

    return pd.DataFrame(doc)

if __name__ == "__main__":
    """
    Точка входа: создает директорию для данных и сохраняет итоговый CSV.
    """
    if not os.path.exists('data'):
        os.makedirs('data')

    df = wiki_corpus()

    df.to_csv('data/corpus.csv', index = False)
    print(f"Собрано абзацев: {len(df)}")
