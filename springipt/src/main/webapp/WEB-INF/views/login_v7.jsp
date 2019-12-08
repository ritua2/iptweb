<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>

<c:set var="contextPath" value="${pageContext.request.contextPath}"/>
<jsp:include page="base.jsp" />


<style>

  .col-container {
    display: table;
    width: 100%;
  }
  .col {
    display: table-cell;
    padding: 0.5%;
  }

  #rcorners_solid {
    border-radius: 0px;
    padding: 2%;
    width: 100%
  }

</style>



<center>
  <div class="col-container" style="width: 95%;">
    <div class="col" style="background: transparent; width: 50%;">
      <h2>What is IPT?</h2>
    </div>

    <div class="col" style="background: transparent; ; width: 50%;">
      <h2>Project News</h2>
    </div>

  </div>
</center>

<br>


<center>
  <div class="col-container" style="width: 95%;">
    <div class="col" style="background:  #f2f3c3; width: 50%;">
      <p>
        Interactive Parallelization Tool (IPT) is a semi-automatic tool that converts a C/C++ serial program into an efficient parallel program by parsing the specification by the users. It is currently being used for teaching parallel programming and supports MPI, OpenMP, and CUDA programming models.
      </p>
      <p>
        You can use IPT from the convenience of your web-browser. It is simple. Start by creating an account on this website or use your existing TACC portal account information.
      </p>
      <p>
        If you login with your TACC portal account credentials, you will be also be able to compile and run the program generated by IPT on two XSEDE systems: Stampede2 and Comet.
      </p>
      <br><br>

      <center>
        <img src="https://www.tacc.utexas.edu/documents/1084364/1748789/stampede-boinc.jpg/" class="img-responsive" height="90%" width="90%">
      </center>
    </div>

    <div class="col" style="background: #e5e5e5 ; width: 50%;">

      <p id="rcorners_solid" style="background-color: #fcfcfc;">
        A tutorial and talk on IPT was hosted at the Terna Engineering College in Mumbai, India on December 2, 2019.
      </p>

      <p id="rcorners_solid" style="background-color: #fcfcfc;">
        A talk on IPT was given at the TACC booth during SC19.
      </p>

      <p id="rcorners_solid" style="background-color: #fcfcfc;">
        A talk on code correctness in parallel programs will be given at the EduHiPC 2019 workshop in Hyderabad, India
      </p>

      <p id="rcorners_solid" style="background-color: #fcfcfc;">
        A tutorial on IPT was held in TACC on October 18th, 2019 event held in Austin, TX.
      </p>

      <p id="rcorners_solid" style="background-color: #fcfcfc;">
        A tutorial on IPT was held at the TACCSTER 2019 event held in Austin, TX.
      </p>

      <p id="rcorners_solid" style="background-color: #fcfcfc;">
        A tutorial on IPT was held in TACC on September 14th, 2017 event held in Austin, TX.
      </p>

    </div>

  </div>
</center>


<jsp:include page="footer.jsp" />
