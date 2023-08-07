def test_elastic(mock_vasp, clean_dir, si_structure):
    import numpy as np
    from jobflow import run_locally
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

    from atomate2.common.schemas.elastic import ElasticDocument
    from atomate2.vasp.flows.elastic import ElasticMaker

    # mapping from job name to directory containing test files
    ref_paths = {
        "elastic relax 1/6": "Si_elastic/elastic_relax_1_6",
        "elastic relax 2/6": "Si_elastic/elastic_relax_2_6",
        "elastic relax 3/6": "Si_elastic/elastic_relax_3_6",
        "elastic relax 4/6": "Si_elastic/elastic_relax_4_6",
        "elastic relax 5/6": "Si_elastic/elastic_relax_5_6",
        "elastic relax 6/6": "Si_elastic/elastic_relax_6_6",
    }

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {
        "elastic relax 1/6": {"incar_settings": ["NSW", "ISMEAR"]},
        "elastic relax 2/6": {"incar_settings": ["NSW", "ISMEAR"]},
        "elastic relax 3/6": {"incar_settings": ["NSW", "ISMEAR"]},
        "elastic relax 4/6": {"incar_settings": ["NSW", "ISMEAR"]},
        "elastic relax 5/6": {"incar_settings": ["NSW", "ISMEAR"]},
        "elastic relax 6/6": {"incar_settings": ["NSW", "ISMEAR"]},
    }

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate flow
    si_prim = SpacegroupAnalyzer(si_structure).get_primitive_standard_structure()
    flow = ElasticMaker().make(si_prim)
    flow.update_maker_kwargs(
        {"_set": {"input_set_generator->user_kpoints_settings->grid_density": 100}},
        name_filter="elastic relax",
        dict_mod=True,
    )

    # Run the flow or job and ensure that it finished running successfully
    responses = run_locally(flow, create_folders=True, ensure_success=True)

    # validation on the outputs
    elastic_output = responses[flow.jobs[-1].uuid][1].output
    assert isinstance(elastic_output, ElasticDocument)
    assert np.allclose(
        elastic_output.elastic_tensor.ieee_format,
        [
            [166.2222, 62.8196, 62.8196, 0.0, 0.0, 0.0],
            [62.8196, 166.2222, 62.8196, 0.0, 0.0, 0.0],
            [62.8196, 62.8196, 166.2222, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 34.5442, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 34.5442, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 34.5442],
        ],
        atol=1e-3,
    )
