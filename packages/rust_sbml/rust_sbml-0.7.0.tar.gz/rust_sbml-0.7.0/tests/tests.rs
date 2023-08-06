use rust_sbml::{
    mathml, mathml::Math, mathml::MathNode, parse_document, Constraint, Message, Model, ModelRaw,
    ModelUnits, UnitSId, UnitSIdRef,
};

#[test]
fn read_units_succeed() {
    let example = include_str!("test_simple.xml");
    let res = parse_document(example);
    assert!(res.is_ok());
    let expect = Model {
        model_units: ModelUnits {
            time_units: Some(UnitSIdRef::SIUnit(UnitSId::second)),
            substance_units: Some(UnitSIdRef::SIUnit(UnitSId::mole)),
            extent_units: Some(UnitSIdRef::SIUnit(UnitSId::mole)),
            ..Default::default()
        },
        ..Default::default()
    };
    assert_eq!(res.unwrap(), expect)
}

#[test]
fn read_model_raw_objective_succeeds() {
    let file_str = include_str!("EcoliCore.xml");
    let model = ModelRaw::parse(file_str).unwrap();
    let gen_file_srt = model.to_string().unwrap();
    println!("{}", gen_file_srt);
    let model = Model::parse(&gen_file_srt).unwrap();

    assert_eq!(
        model
            .objectives
            .unwrap()
            .iter()
            .map(|reac_id| reac_id.to_owned())
            .next()
            .unwrap(),
        "R_BIOMASS_Ecoli_core_w_GAM"
    );
}

#[test]
fn read_abstraction_objective_succeeds() {
    let file_str = include_str!("EcoliCore.xml");
    let model = Model::parse(file_str).unwrap();
    assert_eq!(model.objectives.unwrap()[0], "R_BIOMASS_Ecoli_core_w_GAM");
}

#[test]
fn reaction_annotation_is_parsed() {
    let file_str = include_str!("EcoliCore.xml");
    let model = Model::parse(file_str).unwrap();
    let annot: std::collections::HashMap<&str, Vec<&str>> = model.reactions["R_ACALD"]
        .annotation
        .as_ref()
        .unwrap()
        .into();
    println!("{:?}", annot);
    assert_eq!(annot["bigg.reaction"][0], "ACALD");
}

#[test]
fn model_has_more_species_annotations_species() {
    let file_str = include_str!("EcoliCore.xml");
    let model = Model::parse(file_str).unwrap();
    let annot_len = model
        .species
        .iter()
        .map(|(_, sp)| match sp.annotation.as_ref() {
            Some(rdf) => rdf.into_iter().count(),
            None => 0,
        })
        .sum::<usize>();
    println!("all annots: {:?}", annot_len);
    assert!(annot_len > model.species.len());
}

#[test]
fn model_has_annotations() {
    let file_str = include_str!("EcoliCore.xml");
    let model = Model::parse(file_str).unwrap();
    let annot: std::collections::HashMap<&str, Vec<&str>> =
        model.annotation.as_ref().unwrap().into();
    println!("{:?}", annot);
    assert_eq!(annot["bigg.model"][0], "e_coli_core");
}

#[test]
fn glc_retrieves_corect_formula() {
    let file_str = include_str!("EcoliCore.xml");
    let model = Model::parse(file_str).unwrap();
    let rust_sbml::Species { formula, .. } = &model.species["M_glc__D_e"];
    assert_eq!(formula.as_ref().unwrap(), "C6H12O6");
}

#[test]
fn test_constraints() {
    let example = include_str!("test_constraint.xml");
    let res = parse_document(example).unwrap();
    let expect = Model {
        model_units: ModelUnits {
            time_units: Some(UnitSIdRef::SIUnit(UnitSId::second)),
            substance_units: Some(UnitSIdRef::SIUnit(UnitSId::mole)),
            extent_units: Some(UnitSIdRef::SIUnit(UnitSId::mole)),
            volume_units: None,
            area_units: None,
            length_units: None,
            conversion_factor: None,
        },

        constraints: vec![Constraint {
            math: Some(Math {
                content: MathNode::apply(vec![
                    MathNode::And,
                    MathNode::apply(vec![
                        MathNode::Lt,
                        MathNode::Cn(mathml::Cn {
                            cn_type: mathml::NumberType::Real,
                            content: String::from("1"),
                            base: mathml::Base::default(),
                            definition_url: None,
                            encoding: None,
                            unit: Some(UnitSIdRef::SIUnit(UnitSId::mole)),
                        }),
                        MathNode::Ci {
                            content: "S1".to_owned(),
                            ci_type: None,
                        },
                    ]),
                    MathNode::apply(vec![
                        MathNode::Lt,
                        MathNode::Ci {
                            content: "S1".to_owned(),
                            ci_type: None,
                        },
                        MathNode::Cn(mathml::Cn {
                            cn_type: mathml::NumberType::Real,
                            content: String::from("100"),
                            base: mathml::Base::default(),
                            definition_url: None,
                            encoding: None,
                            unit: Some(UnitSIdRef::SIUnit(UnitSId::mole)),
                        }),
                    ]),
                ]),
            }),
            message: Some(Message {
                content: "Species S1 is out of range.".to_owned(),
            }),
            ..Default::default()
        }],
        ..Default::default()
    };
    assert_eq!(res, expect);
}
