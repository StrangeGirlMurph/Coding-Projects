using UnityEngine;
using UnityEngine.UI;
using System;

public class BoxManager : MonoBehaviour
{
    public int digits = 3;
    public int TimesPerFixedTime = 1000;
    public int numberOfCollisions = 0;
    public Box SmallBox;
    public Box BigBox;
    float sumMass;
    float m1, m2;
    public GameObject wall;
    float leftbound;
    public AudioSource audioSource;
    public Text texty;

    void Awake()
    {
        leftbound = wall.transform.position.x;

        string num = "1";
        num += new String('0', (digits - 1) * 2);
        BigBox.mass = Convert.ToInt64(num);

        m1 = SmallBox.mass;
        m2 = BigBox.mass;
        sumMass = m1 + m2;
    }

    void FixedUpdate()
    {
        texty.text = numberOfCollisions.ToString();
        collisionCheck();
    }

    void collisionCheck()
    {
        for (int i = 0; i < TimesPerFixedTime; i++)
        {

            float SmallBoxleft = SmallBox.positionX - SmallBox.offset;
            float SmallBoxright = SmallBox.positionX + SmallBox.offset;

            float BigBoxleft = BigBox.positionX - BigBox.offset;
            float BigBoxRight = BigBox.positionX + BigBox.offset;

            if (SmallBoxright >= BigBoxleft & SmallBoxleft <= BigBoxRight)
            {
                collisionWithBox();
                numberOfCollisions++;
            }
            if (SmallBoxleft <= leftbound)
            {
                collisionWithWall(SmallBox);
                numberOfCollisions++;
            }

            SmallBox.updatePositionX();
            BigBox.updatePositionX();
        }

    }


    void collisionWithBox()
    {
        float v1 = SmallBox.velocity;
        float v2 = BigBox.velocity;

        SmallBox.velocity = ((m1 - m2) / sumMass) * v1 + ((2 * m2) / sumMass) * v2;
        BigBox.velocity = ((2 * m1) / sumMass) * v1 + ((m2 - m1) / sumMass) * v2;

        playSound();
    }

    void collisionWithWall(Box box)
    {
        box.velocity *= -1;

        playSound();
    }

    void playSound()
    {
        audioSource.Play();
    }
}
