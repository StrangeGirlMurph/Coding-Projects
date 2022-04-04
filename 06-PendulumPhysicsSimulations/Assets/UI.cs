using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI : MonoBehaviour
{
    public Text infoText;
    float acceleration;
    int angle;
    GameObject rod;
    Pendulum script;

    void Start()
    {
        rod = GameObject.Find("Pendulum");
        script = rod.GetComponent<Pendulum>();
    }

    void Update()
    {
        acceleration = script.gravitationalAcceleration;
        angle = (int)(script.angleDeg);
        infoText.text = $"angle: {angle} \ng: {acceleration}";
    }
}
