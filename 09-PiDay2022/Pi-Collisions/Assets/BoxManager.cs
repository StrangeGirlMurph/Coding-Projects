using System;
using UnityEngine;
using UnityEngine.UI;

public class BoxManager : MonoBehaviour
{
    public uint numberOfDigits = 3;
    public uint repetitionsPerFrame = 100;
    public UInt64 numberOfCollisions = 0;
    public Box SmallBox;
    public Box BigBox;
    double sumMass;
    double m1, m2;
    public float leftboundXPosition;
    public AudioSource audioSource;
    public Text textComponent;

    void Awake()
    {
        /* int zeros = (int)((numberOfDigits - 1) * 2);
        string num = "1";
        num += new String('0', zeros);
        BigBox.mass = Convert.ToSingle(num); */
        BigBox.mass = Math.Pow(100, (double)(numberOfDigits - 1));
        m1 = SmallBox.mass;
        m2 = BigBox.mass;
        sumMass = m1 + m2;
    }

    void FixedUpdate()
    {
        textComponent.text = numberOfCollisions.ToString();
        collisionCheck();
    }

    void collisionCheck()
    {
        for (int i = 0; i < repetitionsPerFrame; i++)
        {
            double SmallBoxleft = SmallBox.positionX - SmallBox.offset;
            double SmallBoxright = SmallBox.positionX + SmallBox.offset;

            double BigBoxleft = BigBox.positionX - BigBox.offset;
            double BigBoxRight = BigBox.positionX + BigBox.offset;

            if (SmallBoxright >= BigBoxleft & SmallBoxleft <= BigBoxRight)
            {
                collisionWithBox();
                numberOfCollisions++;
            }
            if (SmallBoxleft <= leftboundXPosition)
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
        double v1 = SmallBox.velocity;
        double v2 = BigBox.velocity;

        SmallBox.velocity = ((m1 - m2) / sumMass) * v1 + ((2 * m2) / sumMass) * v2;
        BigBox.velocity = ((2 * m1) / sumMass) * v1 + ((m2 - m1) / sumMass) * v2;

        //playSound();
    }

    void collisionWithWall(Box box)
    {
        box.velocity *= -1;
        //playSound();
    }

    void playSound()
    {
        audioSource.Play();
    }
}
