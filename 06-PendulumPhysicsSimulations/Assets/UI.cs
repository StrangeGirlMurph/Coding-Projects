using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI : MonoBehaviour
{
    public Text infoText;
    float gravitationalAcceleration;
    int angleDeg;
    GameObject rod;
    Pendulum script;

    void Start()
    {
        rod = GameObject.Find("Pendulum");
        script = rod.GetComponent<Pendulum>();
    }

    void Update()
    {
        gravitationalAcceleration = script.gravitationalAcceleration;
        angleDeg = (int)(script.angleDeg);
        infoText.text = $"angle: {angleDeg} \ng: {gravitationalAcceleration}";
    }
}
