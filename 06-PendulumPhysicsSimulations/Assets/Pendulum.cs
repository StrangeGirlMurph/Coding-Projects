using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class Pendulum : MonoBehaviour
{
    // parameters
    public float gravitationalAcceleration = 9.81f;
    public float massBob = 5f;
    public float lengthRod = 1f;
    public float startingAngleDeg = 70f;
    public float resistance = 0.01f; // 0 equals no friction
    public int repetitionsPerFrame = 100;

    [HideInInspector] public float angleDeg = 0;
    double angle = 0f; // radians
    double angleV = 0f; // m/s
    double angleA = 0f; // m/s^2

    void Start()
    {
        angle = startingAngleDeg * Math.PI / 180;
    }

    void Update()
    {
        float fractionDeltatime = Time.deltaTime / repetitionsPerFrame;

        for (double i = 0; i <= repetitionsPerFrame; i++)
        {
            angleA = getAcceleration(angle, angleV);
            angleV += angleA * fractionDeltatime;
            angle += angleV * fractionDeltatime;
        }

        angleDeg = (float)(angle * 180 / Math.PI);
        transform.rotation = Quaternion.Euler(0f, 0f, angleDeg);
    }

    double getAcceleration(double angle, double angleV)
    {
        return -resistance * angleV - (gravitationalAcceleration / lengthRod) * Math.Sin(angle);
    }
}
