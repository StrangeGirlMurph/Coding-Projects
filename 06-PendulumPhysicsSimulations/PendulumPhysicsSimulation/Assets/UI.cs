using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UI : MonoBehaviour
{
    public Text gText;
    float g;
    int angle;
    GameObject rod;
    Pendulum physics;

    // Start is called before the first frame update
    void Start()
    {
        rod = GameObject.Find("Pendulum");
        physics = rod.GetComponent<Pendulum>();
    }

    // Update is called once per frame
    void Update()
    {
        g = physics.g;
        angle = (int)(physics.angleDeg);
        gText.text = $"angle: {angle} \ng: {g}";
    }
}
