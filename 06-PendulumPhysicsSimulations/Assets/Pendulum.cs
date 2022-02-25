using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class Pendulum : MonoBehaviour
{
    // parameters
    public float g = 9.81f;
    public float mass = 5f;
    public float len = 1f;
   
    public float startingAngleDeg = 70f;
    public float angleDeg = 0;
    float angle = 0f; // in rad
    float angleA = 0f;
    float angleV = 0f;

    // 0 is no friction
    public float resistance = 0.01f;
    
    void Start()
    {
        angle = (float)(startingAngleDeg * Math.PI/180);
    }
    
    void Update()
    {
        float deltatime;
        deltatime = Time.deltaTime;

        angleA = getAcceleration(angle, angleV);
        angleV += angleA * deltatime;
        angle += angleV * deltatime;
        angleDeg = (float)(angle * 180 / Math.PI);

        transform.rotation = Quaternion.Euler(0f, 0f, angleDeg);
    }

    float getAcceleration(float angle, float angleV)
    {
        return -resistance * angleV - (float)((g / len) * Math.Sin(angle));
    }
    
    /*
    void FixedUpdate()
    {
        float deltatime;
        deltatime = Time.fixedDeltaTime;

        angleA = getAcceleration(angle, angleV); 
        angleV += angleA * deltatime;
        angle += angleV * deltatime;
        angleDeg = (float)(angle * 180 / Math.PI);

        transform.rotation = Quaternion.Euler(0f, 0f, angleDeg);
        if (angleDeg == 70)
        {
            Debug.Log(angleDeg);
        }
    } 
    */
}
