using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.InputSystem;

//using Hashtable = ExitGames.Client.Photon.Hashtable;
using UnityEngine.Animations;



public class Enemy : MonoBehaviour
{


    #region Vars
    #region Inspector Reference Vars
    [SerializeField] GameObject cameraHolder;
    [SerializeField] float mouseSenstivity, speed, jumpForce, smoothTime;
    [SerializeField] GameObject itemHolder;
    [SerializeField] GameObject weaponPivot;
    [SerializeField] GameObject Helmet, Body;
    [SerializeField] GameObject playerModel;
    #endregion

    #region Location and Rotation Vars
    private float verticalLookRotation;
    bool grounded;
    Vector3 smoothMoveVelocity;
    Vector3 moveAmount;

    Vector3 moveDir, jumpDir;

    #endregion

    #region Player Vars
    Rigidbody rb;
    #endregion

    #region Health Vars
    private const float maxHealth = 45f;
    private float currentHealth = maxHealth;
    private int healthRechargeWait = 10;
    private int healthRechargePerSecond = 9;
    #endregion
    #endregion

    public float horizontalMovement;
    public float verticalMovement;
    private float distToGround = 0.2f;

    private float maxSpeed = 40;

    private Animator animator;

    private State currentState;
    private UnityEngine.AI.NavMeshAgent nav;
    private GameObject[] locations;
    private int currentLocationIndex;
    private GameObject currentLocation, player;

    public enum State
    {
        CHASING,
        WANDERING,
        STOPPED,
        SEARCHING
    }
    // Start is called before the first frame update
    void Start()
    {
        rb = gameObject.GetComponent<Rigidbody>();
        distToGround = gameObject.GetComponent<MeshCollider>().bounds.extents.y;
        animator = gameObject.GetComponent<Animator>();

        player = GameObject.Find("PlayerBear");
        nav = GetComponent<UnityEngine.AI.NavMeshAgent>();
        locations = new GameObject[3];
        locations[0] = GameObject.Find("Waypoint0");
        locations[1] = GameObject.Find("Waypoint1");
        locations[2] = GameObject.Find("Waypoint2");

    }

    public IEnumerator Search()
    {
        currentState = State.SEARCHING;
        nav.isStopped = true;

        yield return new WaitForSeconds(2);
    }

    /// <summary>
    /// Update method called continously based on frame rate of user to handle local inputs
    /// </summary>
    private void Update()
    {
        float distance = Vector3.Distance(gameObject.transform.position, player.transform.position);

        if(distance < 50f)
        {
            currentState = State.CHASING;
        }
        if (distance > 50f)
        {
            currentState = State.WANDERING;
        }

        if(nav.remainingDistance < 0.5f && currentState == State.WANDERING)
        {
            currentLocationIndex = (currentLocationIndex + 1) % locations.Length;
            if (!nav.pathPending)
            {
                nav.SetDestination(player.transform.position);
                //nav.SetDestination(locations[currentLocationIndex].transform.position);
            }
        }

        if (currentState == State.STOPPED)
        {
            StartCoroutine("Search");
        }

        if (currentState == State.CHASING)
        {
            nav.isStopped = false;
            nav.SetDestination(player.transform.position);
        }

        // This will detect forward and backward movement
        verticalMovement = Input.GetAxis("Vertical");
        if (verticalMovement < 0)
        {
            animator.SetBool("WalkForward", false);
            animator.SetBool("WalkBackward", true);
        }
        else if (verticalMovement > 0)
        {
            animator.SetBool("WalkForward", true);
            animator.SetBool("WalkBackward", false);
        }
        else
        {
            animator.SetBool("WalkForward", false);
            animator.SetBool("WalkBackward", false);
        }
        // This will detect sideways movement
        horizontalMovement = Input.GetAxis("Horizontal");
        //

        //Make sure that the character only animates the idle animation while paused
        //Animation.SetFloat("InputX", 0);
        //Animation.SetFloat("InputZ", 0);

        //kill player controller if they fall into the void
        if (transform.position.y < -10f)
        {
            //Die();
        }

        //Debug.Log(Input.GetKeyDown(KeyCode.Space));
        if (Input.GetKeyDown(KeyCode.Space))
        {
            //Debug.Log(transform.up * jumpForce);
            jumpDir = transform.up * jumpForce;
            animator.SetBool("Jump", true);
        }
        else
        {
            animator.SetBool("Jump", false);
        }
        //Debug.Log(transform.forward * verticalMovement);

        moveDir = transform.forward * verticalMovement + transform.right * horizontalMovement;
        moveDir.Normalize();
    }

    /// <summary>
    /// Method is called at a fixed rate instead of being tied to framerate like update() to move the character model around the game
    /// </summary>
    private void FixedUpdate()
    {
        
    }


    private void attack()
    {
        if (Input.GetMouseButton(1))
        {
            animator.SetBool("Attack1", true);
            RaycastHit hit;
            Physics.Raycast(transform.position, Vector3.forward, out hit, distToGround);

            hit.transform.gameObject.GetComponent<Enemy>();
        }
    }

    public void damage(int damage)
    {
        currentHealth -= damage;
    }


    public Vector3 RandomNavmeshLocation(float radius)
    {
        Vector3 randomDirection = Random.insideUnitSphere * radius;
        randomDirection += transform.position;
        NavMeshHit hit;
        Vector3 finalPosition = Vector3.zero;
        if (NavMesh.SamplePosition(randomDirection, out hit, radius, 1))
        {
            finalPosition = hit.position;
        }
        return finalPosition;
    }
}