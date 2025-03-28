#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from ttr03_flow.crews.poem_crew.poem_crew import PoemCrew


class PoemState(BaseModel):
    sentence_count: int = 1
    topic : str = ""
    poem: str = ""


class PoemFlow(Flow[PoemState]):

    @start()
    def generate_sentence_count(self):
        print("Satır sayısı oluşturuluyor")
        # self.state.sentence_count = randint(1, 5)
        self.state.sentence_count = 10

    @listen(generate_sentence_count)
    def generate_topic(self):
        print("Konu oluşturuluyor")
        self.state.topic = "Tunceli Şehri"

    @listen(generate_topic)
    def generate_poem(self):
        print("Şiir oluşturuluyor")
        result = (
            PoemCrew()
            .crew()
            .kickoff(inputs={"sentence_count": self.state.sentence_count, "topic": self.state.topic})
        )

        print("Şiir oluşturuldu", result.raw)
        self.state.poem = result.raw

    @listen(generate_poem)
    def save_poem(self):
        print("Şiir kaydediliyor")
        with open("poem.txt", "w") as f:
            f.write(self.state.poem)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
